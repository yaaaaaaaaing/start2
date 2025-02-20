import requests
from init import *
from gitpush_if import *


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
    
    # change_file_list = [wechat_token_path]
    # commit_message = "更新 wechat access_token"
    # push_database_to_github(change_file_list,commit_message,secret_path)

def update_external_userid(wechat_extid_path,access_token_func):
    url_ext_list_id = f"https://qyapi.weixin.qq.com/cgi-bin/externalcontact/list?access_token={access_token_func}&userid=LiYang"
    response = requests.get(url_ext_list_id)
    update_ext_id_list = response.json()["external_userid"]

    with open(wechat_extid_path, 'r') as f:
        wechat_extid_dict = json.load(f)
    ext_id_list = wechat_extid_dict["ext_id_list"]
    for update_ext_id in update_ext_id_list:
        if update_ext_id not in ext_id_list:
            ext_id_list.append(update_ext_id)
            url_ext_get = f"https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get?access_token={access_token_func}&external_userid={update_ext_id}"
            update_data_ext_info = requests.get(url_ext_get).json()
            update_client_email = update_data_ext_info["follow_user"][0]["description"]

if __name__ == '__main__':
    # database_branch = "develop"
    # pull_database_from_github(config_path,database_branch)
    access_token_list,access_token_func = get_access_token(wechat_corp_id,wechat_list_secret,wechat_func_secret)
    updata_access_token(access_token_list,access_token_func,wechat_token_path,secret_path)

