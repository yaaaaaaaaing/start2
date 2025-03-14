# -*- coding: utf-8 -*-
import json
import datetime
from register_check_if import *
from send_receive_email import *
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
            for row in range(1,max_row):
                if name_list_ws.cell(row=row,column=expire_column).value == client:
                    name_list_ws.cell(row=row,column=expire_column).value = None
                    if mapping_dict[type]["pin in name list"] is not None:
                        pin_column = mapping_dict[type]["pin in name list"]
                        name_list_ws.cell(row=row,column=pin_column).value = None
                        coordinate_list.append({"row":row,"column":pin_column})
    name_list_wb.save(name_list_path)
    return coordinate_list

def expiration_management_email_send(coordinate_list,server_email):
    body = "需要处理的过期PIN包括：\n"
    for coordinate in coordinate_list:
        body += str(coordinate) + "\n"
    send_email("过期账号待操作", body, server_email, attachments=[])


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
            if datetime.datetime.now() > str_to_datetime(expiration_date) - datetime.timedelta(days=1) and datetime.datetime.now() < str_to_datetime(expiration_date):
                if client_email not in expiration_notification_dict:
                    expiration_notification_dict[client_email] = {}
                    expiration_notification_dict[client_email]["message"] = "一支穿云箭：\n你好\n,"
                    expiration_notification_dict[client_email]["type_list"] = []
                    expiration_notification_dict[client_email]["message"] += f"你的{type}即将于{expiration_date}过期，如果需要请及时续费！\n"
                    expiration_notification_dict[client_email]["type_list"].append(type)
                else:
                    expiration_notification_dict[client_email]["message"] += f"你的{type}即将于{expiration_date}过期，如果需要请及时续费！\n"
                    expiration_notification_dict[client_email]["type_list"].append(type)
            elif datetime.datetime.now() > str_to_datetime(expiration_date) and datetime.datetime.now() < str_to_datetime(expiration_date) + datetime.timedelta(days=1):
                if client_email not in expiration_conformation_dict:
                    expiration_conformation_dict[client_email] = {}
                    expiration_conformation_dict[client_email]["message"] = "一支穿云箭：\n你好\n,"
                    expiration_conformation_dict[client_email]["type_list"] = []
                    expiration_conformation_dict[client_email]["message"] += f"你的{type}已于{expiration_date}过期，如果需要请及时续费！\n"
                    expiration_conformation_dict[client_email]["type_list"].append(type)
                else:
                    expiration_conformation_dict[client_email]["message"] += f"你的{type}已于{expiration_date}过期，如果需要请及时续费！\n"
                    expiration_conformation_dict[client_email]["type_list"].append(type)

    return expiration_notification_dict,expiration_conformation_dict

def check_server_expiration(client_conf_path):
    check_server_results= "attention: \n"
    with open(client_conf_path, 'r') as file:
        client_config_dict = json.load(file)
    for client_info in client_config_dict.values():
        for type,type_info in mapping_dict.items():
            if type_info["server email tag in name list"] in client_info and str_to_datetime(client_info[type_info["server expiration data in name list"]]) - datetime.datetime.now() <= datetime.timedelta(days=3):
                check_server_results += f"你的账号{type}类型账号{client_info[type_info['server email tag in name list']]}即将于{client_info[type_info['server expiration data in name list']]}过期，请及时续费！\n"
                
    return check_server_results
            

def expiration_email_send(expiration_notification_dict,expiration_conformation_dict,check_server_results,server_email):
    for client_email,expiration_info in expiration_notification_dict.items():
        send_email("账号即将过期提醒", expiration_info["message"], client_email, attachments=[])
        send_message_to_external_user(client_email, expiration_info["message"],wechat_extid_path,wechat_token_path)
    for client_email,expiration_info in expiration_conformation_dict.items():
        send_email("账号已过期提醒", expiration_info["message"], client_email, attachments=[])
        # send_message_to_external_user(client_email, expiration_info["message"],wechat_extid_path,wechat_token_path)
    if check_server_results != "attention: \n":
        send_email("服务器账号即将过期提醒", check_server_results, server_email, attachments=[])
        error_report_wechat(check_server_results,wechat_extid_path,wechat_token_path)

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "expire_type:", ["expire_type="])
    except getopt.GetoptError as err:
        print(f"Error: {err}")
        exit(1)
    
    expire_type = "dailycheck"

    # 解析参数
    for opt, value in opts:
        if opt in ("-e", "--expire_type"):
            expire_type = value

    database_branch = "ubuntu"
    pull_database_from_github(config_path,database_branch)
    expiration_notification_dict,expiration_conformation_dict = check_client_expiration(expiration_dict_path)
    check_server_results = check_server_expiration(client_conf_path)
    if expire_type == "dailycheck":
        expiration_email_send(expiration_notification_dict,expiration_conformation_dict,check_server_results,server_email)
        print("Expiration check finished.")

    if expire_type == "management":
        coordinate_list = name_list_expire_gen(name_list_path,expiration_conformation_dict)
        expire_client_expiration(expiration_conformation_dict,expiration_dict_path)
        updata_name_list(name_list_path,client_conf_path,hash_path)
        commit_message = "expiration infos removed"
        # gitpush_json(config_path,hash_path,name_list_path,commit_message)
        expiration_management_email_send(coordinate_list,server_email)