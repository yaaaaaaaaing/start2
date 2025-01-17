import os
import time
import glob
import hashlib
import json
from init import *
import subprocess


def pull_database_from_github(config_path,database_branch):
    if any(os.scandir(config_path)) is False:
        subprocess.call(f"git submodule update --init --recursive", shell=True)
        subprocess.call(f"git checkout {database_branch}", shell=True,cwd=config_path)
        print("git checkout submodules mannually")

def hash_check(config_path,file_type,hash_json_file): # 检查json文件是否发生变化
    with open(hash_json_file, 'r') as hash_file:
        hash_dict = json.load(hash_file)

    change_file_list = []
    file_list = glob.glob(config_path + "/*." + file_type)
    hash_update_dict = {}
    for file in file_list:
        if "hash.json" not in file:
            file_str = open(file, 'rb').read()
            file_hash = hashlib.md5(file_str).hexdigest()
            file_name = os.path.basename(file)
            hash_update_dict[file_name] = file_hash

            if file_name not in hash_dict.keys():
                change_file_list.append(file)
            elif file_hash != hash_dict[file_name]:
                change_file_list.append(file)
    
    with open(hash_json_file, 'w') as hash_file:
        json.dump(hash_update_dict, hash_file, indent=4)

    return change_file_list

def push_database_to_github(change_file_list,name_list_path,hash_json_file,commit_message,config_path):
    change_file_list.append(hash_json_file)
    change_file_list.append(name_list_path)
    for file in change_file_list:
        try:
            #将相对config_path的路径添加到submodule中
            subprocess.call(f"git add {os.path.relpath(file, config_path)}", shell=True,cwd=config_path)
        except:
            continue
    subprocess.call("git status", shell=True, cwd=config_path)
    commit = f'git commit -m "{commit_message}"'
    subprocess.call(commit, shell=True,cwd=config_path)
    subprocess.call("git status", shell=True, cwd=config_path)
    subprocess.call("git config --get remote.origin.url ", shell=True, cwd=config_path)
    subprocess.call("git remote set-url --push origin git@github.com:yaaaaaaaaing/start2_database.git", shell=True, cwd=config_path)
    subprocess.call("git push origin HEAD", shell=True,cwd=config_path)
    subprocess.call("git status", shell=True, cwd=config_path)

def gitpush_json(config_path,hash_path,name_list_path,commit_message):
    change_file_list = hash_check(config_path,"json",hash_path)
    if len(change_file_list) > 0:
        push_database_to_github(change_file_list,name_list_path,hash_path,commit_message,config_path)