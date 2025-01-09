# -*- coding: utf-8 -*-
import datetime
import json
from init import *
from name_list_if import *
from gitpush_if import *

def datetime_to_str(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")
def str_to_datetime(s):
    return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

# 新增或续费时调用，更新expiration dict
def update_client_expiration(register_check_dict,expiration_dict_path):
    with open(expiration_dict_path, 'r') as file:
        expiration_dict = json.load(file)
    for client_email,type_info_list in register_check_dict.items():
        for type_info in type_info_list:
            if type_info["days"] > 0:
                if client_email in expiration_dict:
                    if type_info["type"] in expiration_dict[client_email]["expiration_list"]:
                        expiration_dict[client_email]["history_list"][type_info["type"]].append(expiration_dict[client_email]["expiration_list"][type_info["type"]])
                        expiration_dict[client_email]["expiration_list"][type_info["type"]] = datetime_to_str(max(datetime.datetime.now(),str_to_datetime(expiration_dict[client_email]["expiration_list"][type_info["type"]])) + datetime.timedelta(days=type_info["days"]) )    
                    else:
                        # 对于新增的数据类型，初始化history list，新建expiration list
                        expiration_dict[client_email]["history_list"][type_info["type"]] = []
                        expiration_dict[client_email]["expiration_list"][type_info["type"]] = datetime_to_str(datetime.datetime.now() + datetime.timedelta(days=type_info["days"]))
                else:
                    expiration_dict[client_email] = {
                        "history_list": {type_info["type"]: []},
                        "expiration_list": {type_info["type"]: datetime_to_str(datetime.datetime.now() + datetime.timedelta(days=type_info["days"]))}
                    }
    with open(expiration_dict_path, 'w') as file:
        json.dump(expiration_dict, file, indent=4)     

def add_account_to_name_list(register_check_dict,name_list_path):
    name_list_wb = openpyxl.load_workbook(name_list_path)
    name_list_ws = name_list_wb["list"]

    for client_email,type_info_list in register_check_dict.items():
        for type_info in type_info_list:
            if type_info["days"] > 0:
                check_account_flag = False
                for row in range(2,name_list_ws.max_row):
                    if client_email == name_list_ws.cell(row,mapping_dict[type_info["type"]]["client in name list"]).value:
                        check_account_flag = True
                        break
                if check_account_flag == False:
                    add_account_flag = False
                    server_expiration = datetime.datetime.now()
                    for row in range(2,name_list_ws.max_row):
                        temp_server_expiration = name_list_ws.cell(row,mapping_dict[type_info["type"]]["expiration data in name list"]).value
                        server_expiration = temp_server_expiration if temp_server_expiration != None else server_expiration
                        if server_expiration > datetime.datetime.now() and name_list_ws.cell(row,mapping_dict[type_info["type"]]["client in name list"]).value == None:
                            name_list_ws.cell(row,mapping_dict[type_info["type"]]["client in name list"]).value = client_email
                            add_account_flag = True
                            break
                    if add_account_flag == False:
                        print("No empty row in name list, one more server email should be registered.")
                        exit()

    name_list_wb.save(name_list_path)

def add_account_to_codecheck_dict(client_email,client_conf_path,code_check_dict_path,mapping_dict):
    with open(client_conf_path, 'r') as file:
        client_conf_info = json.load(file)
    with open(code_check_dict_path, 'r') as file:
        code_check_dict = json.load(file)
    if client_email not in code_check_dict:
        code_check_dict[client_email] = {}
    for type,type_info in mapping_dict:
        if type_info["server email tag in name list"] in client_conf_info[client_email]:
            if type not in code_check_dict[client_email]:
                code_check_dict[client_email][type] = {"server email":client_conf_info[client_email][type_info["server email tag in name list"]],"check timer": 0}

if __name__ == '__main__':
    client_email = "liyang.tjtj@gmail.com"
    type_info_list = [{"type":"vpn_account","days":0},{"type":"nf_account","days":0}]
    register_check_dict = {}
    register_check_dict[client_email] = type_info_list
    


    update_client_expiration(register_check_dict,expiration_dict_path)
    add_account_to_name_list(register_check_dict,name_list_path)