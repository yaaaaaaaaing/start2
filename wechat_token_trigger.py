import requests
from init import *
from gitpush_if import *


def get_access_token(corp_id,corp_secret):
    url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={corp_secret}'
    response = requests.get(url)
    data = response.json()
    if data.get("errcode") == 0:
        return data["access_token"]
    else:
        raise Exception(f"获取 access_token 失败，错误信息：{data.get('errmsg')}")

def updata_access_token(access_token,wechat_token_path,secret_path):
    with open(wechat_token_path, 'w') as f:
        f.write(access_token)
    
    change_file_list = [wechat_token_path]
    commit_message = "更新 wechat access_token"
    push_database_to_github(change_file_list,commit_message,secret_path)
    

if __name__ == '__main__':
    database_branch = "develop"
    pull_database_from_github(config_path,database_branch)
    access_token = get_access_token(wechat_corp_id,wechat_corp_secret)
    updata_access_token(access_token,wechat_token_path,secret_path)

