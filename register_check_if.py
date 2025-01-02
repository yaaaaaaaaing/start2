import datetime
import json
from init import *

def datetime_to_str(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")
def str_to_datetime(s):
    return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

# 新增或续费时调用，更新name list + deadline dict
def update_deadline(client_email,type_info_list,deadline_dict_path):
    with open(deadline_dict_path, 'r') as file:
        deadline_dict = json.load(file)
    if client_email in deadline_dict:
        for type_info in type_info_list:
            if type_info["type"] in deadline_dict[client_email]["deadline_list"]:
                deadline_dict[client_email]["history_list"][type_info["type"]].append(deadline_dict[client_email]["deadline_list"][type_info["type"]])
                deadline_dict[client_email]["deadline_list"][type_info["type"]] = datetime_to_str(max(datetime.datetime.now(),str_to_datetime(deadline_dict[client_email]["deadline_list"][type_info["type"]])) + datetime.timedelta(days=type_info["days"]) )    
            else:
                deadline_dict[client_email]["history_list"][type_info["type"]] = []
                deadline_dict[client_email]["deadline_list"][type_info["type"]] = datetime_to_str(datetime.datetime.now() + datetime.timedelta(days=type_info["days"]))
    else:
        deadline_dict[client_email] = {
            "history_list": {type_info["type"]: [] for type_info in type_info_list},
            "deadline_list": {type_info["type"]: None for type_info in type_info_list}
        }
        for type_info in type_info_list:
            deadline_dict[client_email]["deadline_list"][type_info["type"]] = datetime_to_str(datetime.datetime.now() + datetime.timedelta(days=type_info["days"]))
    with open(deadline_dict_path, 'w') as file:
        json.dump(deadline_dict, file, indent=4)      


if __name__ == '__main__':
    client_email = "993313387@qq.com"
    type_info_list = [{"type":"vpn account","days":10},{"type":"nf account","days":20}]
    update_deadline(client_email,type_info_list,deadline_dict_path)