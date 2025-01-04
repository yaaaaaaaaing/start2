# -*- coding: utf-8 -*-
import json
import datetime
from register_check_if import *

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

def expiration_email_send(expiration_notification_dict,expiration_conformation_dict):
    for client_email,expiration_info in expiration_notification_dict.items():
        send_email("账号即将过期提醒", expiration_info["message"], client_email, attachments=[])
    for client_email,expiration_info in expiration_conformation_dict.items():
        send_email("账号已过期提醒", expiration_info["message"], client_email, attachments=[])

if __name__ == "__main__":
    expiration_notification_dict,expiration_conformation_dict = check_client_expiration(expiration_dict_path)
    expiration_email_send(expiration_notification_dict,expiration_conformation_dict)
    print("Expiration check finished.")