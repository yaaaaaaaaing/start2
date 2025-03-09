import getopt
import json
from init import *
import sys
import traceback

def reset_client_code_info(client_email,check_type,code_check_dict_path):
    with open(code_check_dict_path, 'r') as code_check_file:
        json_data = json.load(code_check_file)  
    json_data[client_email][check_type]["check timer"] = 0

    with open(code_check_dict_path, 'w') as code_check_file:
        json.dump(json_data, code_check_file, indent=4)
    print(f"{client_email} code check data {check_type} is reset")

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "e:t:", ["email=", "type="])
    except getopt.GetoptError as err:
        print(f"Error: {err}")
        exit(1)
    
    client_email = ""
    check_type = ""

    # 解析参数
    for opt, value in opts:
        if opt in ("-e", "--email"):
            client_email = value
        elif opt in ("-t", "--type"):
            check_type = value

    reset_client_code_info(client_email,check_type,code_check_dict_path)