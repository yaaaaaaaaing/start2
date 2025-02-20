import getopt
import sys
import json
from send_receive_email import *

if __name__ == "__main__":
    # try:
    #     opts, args = getopt.getopt(sys.argv[1:], "e:t:", ["email=", "type="])
    # except getopt.GetoptError as err:
    #     print(f"Error: {err}")
    #     exit(1)
    
    # client_email = ""
    # check_type = ""

    # # 解析参数
    # for opt, value in opts:
    #     if opt in ("-e", "--email"):
    #         client_email = value
    #     elif opt in ("-t", "--type"):
    #         check_type = value

    # output = "begin\n"
    # output += f"Client Email: {client_email}\nCheck Type: {check_type}"
    # with open("/tmp/ubuntu_test.txt", "w") as f:
    #     f.write(output)

    with open("./secrets/access_token.json") as f:
        access_token_dict = json.load(f)
        access_token_list = access_token_dict["access_token_list"]
        access_token_func = access_token_dict["access_token_func"]

    # url_list_id = f"https://qyapi.weixin.qq.com/cgi-bin/user/list_id?access_token={access_token_list}"
    # json_list_id = {
    #     "cursor": "",
	#     "limit": 10000
    # }
    # response_list_id = requests.post(url_list_id, json=json_list_id)
    # data_list_id = response_list_id.json()

    url_ext_list_id = f"https://qyapi.weixin.qq.com/cgi-bin/externalcontact/list?access_token={access_token_func}&userid=LiYang"
    response_ext_list_id = requests.get(url_ext_list_id)
    data_ext_list_id = response_ext_list_id.json()

    external_user_id_list = data_ext_list_id["external_userid"]
    external_user_id_test = external_user_id_list[0]
    url_ext_get = f"https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get?access_token={access_token_func}&external_userid={external_user_id_test}"
    data_ext_info = requests.get(url_ext_get).json()

    # user_id = "LiYang"
    # message = "test message"
    # send_message_to_external_user(access_token_func, user_id, message)
    print(1)