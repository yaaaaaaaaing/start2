import requests
import json
import base64
import imaplib
import email
from email.header import decode_header
import re
from init import mapping_dict


def get_client_code_info(client_email,check_type,proxy_addr,proxy_port):
    url = f"https://raw.githubusercontent.com/yaaaaaaaaing/start2_database/refs/heads/develop/code_check_info.json"

    if proxy_addr is not "" and proxy_port is not "":
        proxies = {
        "http": f"http://{proxy_addr}:{proxy_port}",  # HTTP 代理
        "https": f"http://{proxy_addr}:{proxy_port}",  # HTTPS 代理
    }
        response = requests.get(url,proxies=proxies)
    else:
        response = requests.get(url)
    response.raise_for_status()  # 检查请求是否成功
    json_data = response.json()  # 将响应内容解析为 JSON\
    try:
        server_check_info = json_data[client_email][check_type]
        check_timer = server_check_info["check timer"]
        if check_timer >= 2:
            print("The check times has reached the maximum (each client email can check 2 times)")
            exit(1)
    except KeyError:
        print("The registration email or check type does not exist")
        return
    return server_check_info

def update_client_code_info(client_email,check_type,proxy_addr,proxy_port):
    repo_owner = "yaaaaaaaaing" 
    repo_name = "start2_database" 
    file_path = "code_check_info.json" 
    branch = "develop"
    token = ""

    file_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    headers = {"Authorization": f"token {token}"}
    if proxy_addr is not "" and proxy_port is not "":
        proxies = {
        "http": f"http://{proxy_addr}:{proxy_port}",  # HTTP 代理
        "https": f"http://{proxy_addr}:{proxy_port}",  # HTTPS 代理
    }
        response = requests.get(file_url, headers=headers,proxies=proxies)
    else:
        response = requests.get(file_url, headers=headers)
    response.raise_for_status()
    file_info = response.json()
    sha = file_info["sha"] 
    content = base64.b64decode(file_info["content"]).decode("utf-8")
    json_data = json.loads(content)
    
    try:
        json_data[client_email][check_type]["check timer"] += 1
        updated_content = base64.b64encode(json.dumps(json_data, indent=4).encode("utf-8")).decode("utf-8")

        update_data = {
            "message": f"Update timer file triggered by ({client_email})",  
            "content": updated_content, 
            "sha": sha, 
            "branch": branch, 
        }
    except KeyError:
        print("The registration email or check type does not exist")
        return

    if proxy_addr is not "" and proxy_port is not "":
        update_response = requests.put(file_url, headers=headers, json=update_data,proxies=proxies)
        update_response.raise_for_status()
    else:
        update_response = requests.put(file_url, headers=headers, json=update_data)
        update_response.raise_for_status()
    

def receive_gmail_email(server_check_email,server_password):
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
        print("未能获取邮件列表。")
    mail.logout()

    return receive_text_list

def parse_check_code(receive_text_list,server_tag):
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
        print("No check code found, please trigger the check code email again")
        exit(1)
    
    return first_match


if __name__ == "__main__":
    selections_str = ""
    for type in mapping_dict:
        selections_str += type + " "
    client_email = input("Please input the your registration email: ")
    check_type = input(f"Please input the check type ({selections_str}): ")
    proxy_addr = input(f"Please input proxy address:")
    proxy_port = input(f"Please input proxy port:")
    
    server_check_info = get_client_code_info(client_email,check_type,proxy_addr,proxy_port)

    server_check_email = server_check_info["server email"]
    server_password = server_check_info["server email pw"]
    server_tag = server_check_info["tag"]
    receive_text_list = receive_gmail_email(server_check_email,server_password)
    first_match = parse_check_code(receive_text_list,server_tag)


    update_client_code_info(client_email,check_type,proxy_addr,proxy_port)
    print(f"check code is {first_match}")
