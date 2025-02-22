# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

import imaplib
import email
from email.header import decode_header
import requests
import json


def send_message_to_external_user(client_email, message,wechat_extid_path,wechat_token_path):
    with open(wechat_token_path, 'r') as f:
        access_token_dict = json.load(f)
        access_token_func = access_token_dict["access_token_func"]
        f.close()
    with open(wechat_extid_path, 'r') as f:
        wechat_extid_dict = json.load(f)
        f.close()
    if client_email == "SERVER":
        user_id = "LiYang"
    elif client_email in wechat_extid_dict["extid_email_map"]:
        user_id = wechat_extid_dict["extid_email_map"][client_email]
    else:
        err_message = f"warning: No external user ID found for email {client_email}"
        error_report_wechat(err_message,wechat_extid_path,wechat_token_path)
        return

    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token_func}"
    data = {
        "touser": user_id,  # 外部联系人的UserID
        "msgtype": "text",
        "agentid": 1000002,  # 企业应用的 agentid
        "text": {
            "content": message  # 要发送的文本消息
        }
    }
    
    response = requests.post(url, json=data)
    data = response.json()
    if data.get("errcode") == 0:
        print("Message sent successfully!")
    else:
        print(f"Error: {data.get('errmsg')}")

def error_report_wechat(error_report_str,wechat_extid_path,wechat_token_path):
    email = "SERVER"
    message = error_report_str
    send_message_to_external_user(email, message,wechat_extid_path,wechat_token_path)

def send_email(subject, body, to_email, attachments=[]):
    password = "nbfikmyoudedrrju"
    from_email = "niustaat@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    for attachment in attachments:
        attachment_name = os.path.basename(attachment)
        with open(attachment, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={attachment_name}'
            )
            msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # 启用TLS加密
    server.login(from_email, password)
    
    server.sendmail(from_email, to_email, msg.as_string())
    print("邮件发送成功！")

    server.quit()

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
        output_msg += "邮箱状态异常，请联系管理员\n"
    mail.logout()

    return receive_text_list,output_msg


# 使用示例
if __name__ == "__main__":
    subject = "测试邮件"
    body = "你好，这是一封来自Python的测试邮件。"
    to_email = "ceshizhanghao31900@outlook.com"
    attachment = None # 如果没有附件，可以设置为 None

    send_email(subject, body, to_email, attachment)