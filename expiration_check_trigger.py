# -*- coding: utf-8 -*-
import json
import datetime
from register_check_if import *
import getopt
import sys

def name_list_expire_gen(name_list_path,expiration_conformation_dict):
    name_list_wb = openpyxl.load_workbook(name_list_path)
    name_list_ws = name_list_wb["list"]
    max_row = name_list_ws.max_row
    coordinate_list = []
    for client,expire_info in expiration_conformation_dict.items():
        for type in expire_info["type_list"]:
            expire_column = mapping_dict[type]["client in name list"]
            for row in range(max_row):
                if name_list_ws.cell(row=row,column=expire_column).value == client:
                    name_list_ws.cell(row=row,column=expire_column).value = None
                    if mapping_dict[type]["pin in name list"] is not None:
                        pin_column = mapping_dict[type]["pin in name list"]
                        name_list_ws.cell(row=row,column=pin_column).value = None
                        coordinate_list.append({"row":row,"column":pin_column})
    return coordinate_list

def expire_client_expiration(expiration_conformation_dict,expiration_dict_path):
    with open(expiration_dict_path, 'r') as file:
        expiration_dict = json.load(file)
    for client_email,expire_info_list in expiration_conformation_dict.items():
        for type in expire_info_list["type_list"]:
            expiration_dict[client_email]["expiration_list"].pop(type)

    with open(expiration_dict_path, 'w') as file:
        json.dump(expiration_dict, file, indent=4)  

def check_client_expiration(expiration_dict_path):
    expiration_notification_dict = {}
    expiration_conformation_dict = {}   
    with open(expiration_dict_path, 'r') as file:
        expiration_dict = json.load(file)
    for client_email,expiration_info in expiration_dict.items():
        for type,expiration_date in expiration_info["expiration_list"].items():
            if datetime.datetime.now() > str_to_datetime(expiration_date) - datetime.timedelta(days=3) and datetime.datetime.now() < str_to_datetime(expiration_date):
                if client_email not in expiration_notification_dict:
                    expiration_notification_dict[client_email] = {}
                    expiration_notification_dict[client_email]["message"] = "一支穿云箭：\n"
                    expiration_notification_dict[client_email]["type_list"] = []
                    expiration_notification_dict[client_email]["message"] += f"你的{type}即将于{expiration_date}过期，请及时续费！\n"
                    expiration_notification_dict[client_email]["type_list"].append(type)
                else:
                    expiration_notification_dict[client_email]["message"] += f"你的{type}即将于{expiration_date}过期，请及时续费！\n"
                    expiration_notification_dict[client_email]["type_list"].append(type)
            elif datetime.datetime.now() > str_to_datetime(expiration_date):
                if client_email not in expiration_conformation_dict:
                    expiration_conformation_dict[client_email] = {}
                    expiration_conformation_dict[client_email]["message"] = "一支穿云箭：\n"
                    expiration_conformation_dict[client_email]["type_list"] = []
                    expiration_conformation_dict[client_email]["message"] += f"你的{type}已于{expiration_date}过期，请及时续费！\n"
                    expiration_conformation_dict[client_email]["type_list"].append(type)
                else:
                    expiration_conformation_dict[client_email]["message"] += f"你的{type}已于{expiration_date}过期，请及时续费！\n"
                    expiration_conformation_dict[client_email]["type_list"].append(type)

    return expiration_notification_dict,expiration_conformation_dict

def expiration_email_send(expiration_notification_dict,expiration_conformation_dict,server_email):
    for client_email,expiration_info in expiration_notification_dict.items():
        send_email("账号即将过期提醒", expiration_info["message"], client_email, attachments=[])
    for client_email,expiration_info in expiration_conformation_dict.items():
        send_email("账号已过期提醒", expiration_info["message"], client_email, attachments=[])

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "expire_type:", ["expire_type="])
    except getopt.GetoptError as err:
        print(f"Error: {err}")
        exit(1)
    
    expire_type = ""

    # 解析参数
    for opt, value in opts:
        if opt in ("-e", "--expire_type"):
            expire_type = value

    database_branch = "develop"
    pull_database_from_github(config_path,database_branch)
    expiration_notification_dict,expiration_conformation_dict = check_client_expiration(expiration_dict_path)
    # expiration_email_send(expiration_notification_dict,expiration_conformation_dict,server_email)
    print("Expiration check finished.")

    if expire_type == "management":
        coordinate_list = name_list_expire_gen(name_list_path,expiration_conformation_dict)
        expire_client_expiration(expiration_conformation_dict,expiration_dict_path)
        updata_name_list(name_list_path,client_conf_path,hash_path)
        commit_message = "expiration infos removed"
        # gitpush_json(config_path,hash_path,name_list_path,commit_message)