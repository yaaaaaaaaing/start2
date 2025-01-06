# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import imaplib
import email
from email.header import decode_header

def send_email(subject, body, to_email, attachments=[]):
    password = "nbfikmyoudedrrju"
    from_email = "niustaat@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    for attachment in attachments:
        with open(attachment, 'rb') as file:
            part = MIMEBase('application', 'pdf')
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={attachment.split("/")[-1]}'
            )
            msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # 启用TLS加密
    server.login(from_email, password)
    
    server.sendmail(from_email, to_email, msg.as_string())
    print("邮件发送成功！")

    server.quit()

def receive_email():
    imap_server = "imap.gmail.com"
    email_user = "niustaat@gmail.com" 
    email_password = "nbfikmyoudedrrju"

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
                                body = part.get_payload(decode=True).decode()
                                receive_text_list.append(body)

                    else:
                        content_type = msg.get_content_type()
                        if content_type == "text/plain":
                            body = msg.get_payload(decode=True).decode()
                            receive_text_list.append(body)
    else:
        print("未能获取邮件列表。")
    mail.logout()

    return receive_text_list


# 使用示例
if __name__ == "__main__":
    subject = "测试邮件"
    body = "你好，这是一封来自Python的测试邮件。"
    to_email = "ceshizhanghao31900@outlook.com"
    attachment = None # 如果没有附件，可以设置为 None

    send_email(subject, body, to_email, attachment)