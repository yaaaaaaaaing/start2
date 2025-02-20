import requests
from init import *
from gitpush_if import *
from send_receive_email import *

def get_access_token(corp_id,wechat_list_secret,wechat_func_secret):
    url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={wechat_list_secret}'
    response = requests.get(url)
    data = response.json()
    access_token_list = data["access_token"]

    url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={wechat_func_secret}'
    response = requests.get(url)
    data = response.json()
    access_token_func = data["access_token"]

    return access_token_list,access_token_func

def updata_access_token(access_token_list,access_token_func,wechat_token_path,secret_path):
    access_token_dict = {
        "access_token_list":access_token_list,
        "access_token_func":access_token_func
    }
    with open(wechat_token_path, 'w') as f:
        f.write(json.dumps(access_token_dict, indent=2, ensure_ascii=False))
        f.close()

def update_external_userid(wechat_extid_path,wechat_token_path,client_conf_path):
    with open(client_conf_path, 'r') as f:
        client_conf_dict = json.load(f)
        f.close()
    with open(wechat_token_path, 'r') as f:
        access_token_dict = json.load(f)
        access_token_func = access_token_dict["access_token_func"]
    url_ext_list_id = f"https://qyapi.weixin.qq.com/cgi-bin/externalcontact/list?access_token={access_token_func}&userid=LiYang"
    response = requests.get(url_ext_list_id)
    update_ext_id_info = response.json()
    update_ext_id_list = update_ext_id_info["external_userid"]

    with open(wechat_extid_path, 'r') as f:
        wechat_extid_dict = json.load(f)
        f.close()
    ext_id_list = wechat_extid_dict["ext_id_list"]

    for update_ext_id in update_ext_id_list:
        if update_ext_id not in ext_id_list:
            url_ext_get = f"https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get?access_token={access_token_func}&external_userid={update_ext_id}"
            update_data_ext_info = requests.get(url_ext_get).json()
            update_client_email = update_data_ext_info["follow_user"][0]["description"]
            if update_client_email not in wechat_extid_dict["extid_email_map"]:
                if update_client_email in client_conf_dict:
                    ext_id_list.append(update_ext_id)
                    wechat_extid_dict["extid_email_map"][update_client_email] = update_ext_id
                elif update_client_email is not "":
                    ext_mark = update_data_ext_info["follow_user"][0]["remark"]
                    error_report_str = f"Error: {ext_mark} is not in client info"
                    error_report_wechat(error_report_str,access_token_func)
    
    emails_to_remove = []
    for ext_id in ext_id_list:
        if ext_id not in update_ext_id_list:
            ext_id_list.remove(ext_id)
            for email,id in wechat_extid_dict["extid_email_map"].items():
                if id == ext_id:
                    emails_to_remove.append(email)
    for email in emails_to_remove:
        wechat_extid_dict["extid_email_map"].pop(email)
                
    
    with open(wechat_extid_path, 'w') as f:
        f.write(json.dumps(wechat_extid_dict, indent=2, ensure_ascii=False))
        f.close()
    
    print("update external_userid successfully")

if __name__ == '__main__':
    access_token_list,access_token_func = get_access_token(wechat_corp_id,wechat_list_secret,wechat_func_secret)
    updata_access_token(access_token_list,access_token_func,wechat_token_path,secret_path)
    update_external_userid(wechat_extid_path,wechat_token_path,client_conf_path)

