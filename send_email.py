import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(subject, body, to_email, attachments=[]):
    password = "nbfikmyoudedrrju"
    from_email = "niustaat@gmail.com"
    try:
        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # 添加邮件正文
        msg.attach(MIMEText(body, 'plain'))
        
        # 如果有附件，添加附件
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
        
        # 连接到Outlook SMTP服务器
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # 启用TLS加密
        server.login(from_email, password)  # 登录邮箱
        
        # 发送邮件
        server.sendmail(from_email, to_email, msg.as_string())
        print("邮件发送成功！")
        
        # 关闭服务器
        server.quit()
    except Exception as e:
        print(f"发送失败: {e}")

# 使用示例
if __name__ == "__main__":
    subject = "测试邮件"
    body = "你好，这是一封来自Python的测试邮件。"
    to_email = "ceshizhanghao31900@outlook.com"
    attachment = None # 如果没有附件，可以设置为 None

    send_email(subject, body, to_email, attachment)