import getopt
import json
import imaplib
import email
from email.header import decode_header
import re
from init import *
from gitpush_if import *
import sys
import requests
from send_receive_email import *


def get_client_code_info(client_email,check_type,code_check_dict_path,output_message):
    output_msg = output_message
    with open(code_check_dict_path, 'r') as code_check_file:
        code_check_dict = json.load(code_check_file)
    server_check_info = code_check_dict[client_email][check_type]
    check_timer = server_check_info["check timer"]
    if check_timer >= 2:
        output_msg += "当前限制验证码登陆次数为2次\n"
    return server_check_info,output_msg

def update_client_code_info(client_email,check_type,code_check_dict_path):
    with open(code_check_dict_path, 'r') as code_check_file:
        json_data = json.load(code_check_file)  
    json_data[client_email][check_type]["check timer"] += 1
    
    with open(code_check_dict_path, 'w') as code_check_file:
        json.dump(json_data, code_check_file, indent=4)

    

def receive_gmail_email(server_check_email,server_password,output_message):
    output_msg = output_message
    imap_server = "imap.gmail.com"
    email_user = server_check_email
    email_password = server_password

    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_user, email_password)
    mail.select("inbox")
    status, messages = mail.search(None, 'UNSEEN')  # 'UNSEEN' 表示未读邮件

    receive_text_list = []
    if status == "OK":
        mail_ids = messages[0].split()

        for mail_id in mail_ids:
            res, msg = mail.fetch(mail_id, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                body = part.get_payload(decode=True).decode(encoding if encoding else "utf-8")  
                    else:
                        content_type = msg.get_content_type()
                        if content_type == "text/plain":
                            body = msg.get_payload(decode=True).decode(encoding if encoding else "utf-8")
                    receive_text_list.append({"subject":subject,"body":body})                          
    else:
        output_msg += "未能获得包含验证码的邮件\n"
    mail.logout()

    return receive_text_list,output_msg

def parse_check_code(receive_text_list,server_tag,output_message):
    output_msg = output_message
    first_match = ""
    pattern = r"^\d{4}$"
    flag_code_found = False
    for receive_text_info in receive_text_list:
        if server_tag in receive_text_info["subject"]:
            body_str_list = receive_text_info["body"].split()
            for body_str in body_str_list:
                if re.fullmatch(pattern, body_str):
                    first_match = body_str
                    flag_code_found = True
                    break
    if flag_code_found == False:
        output_msg += "未能获得验证码\n"
    
    return first_match,output_msg

def post_code_message(output_message):
    response = requests.post("http://localhost:1234/display_output", data={"message": output_message})
    if response.status_code == 200:
        print("信息已发送到网页。")
    else:
        print("信息发送失败。")
    


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



    database_branch = "develop"
    output_message = ""
    pull_database_from_github(config_path,database_branch)
    server_check_info,output_message = get_client_code_info(client_email,check_type,code_check_dict_path,output_message)
    
    server_check_email = server_check_info["server email"]
    server_password = server_check_info["server email pw"]
    server_tag = server_check_info["tag"]
    commit_message = f"check code for {client_email}"
    receive_text_list,output_message = receive_gmail_email(server_check_email,server_password,output_message)
    first_match,output_message = parse_check_code(receive_text_list,server_tag,output_message)

    # post_code_message(output_message)
    if first_match != "" and output_message == "":
        update_client_code_info(client_email,check_type,code_check_dict_path)
        gitpush_json(config_path,hash_path,name_list_path,commit_message)
        subject = "验证码信息"
        send_email(subject, first_match, client_email, [])
    else:
        subject = "验证码信息"
        send_email(subject, output_message, client_email, [])
