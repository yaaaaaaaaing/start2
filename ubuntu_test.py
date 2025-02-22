import getopt
import sys
import json
from send_receive_email import *
from init import *

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

    output = "begin\n"
    output += f"Client Email: {client_email}\nCheck Type: {check_type}"
    with open("./tmp/ubuntu_test.txt", "w+") as f:
        f.write(output)

    error_report_str = "test finish"
    error_report_wechat(error_report_str,wechat_extid_path,wechat_token_path)

    print(1)