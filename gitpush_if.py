import os
import time
import glob
import hashlib
import json
from init import *
import subprocess


def hash_check(file_path,file_type,hash_json_file): # 检查json文件是否发生变化
    with open(hash_json_file, 'r') as hash_file:
        hash_dict = json.load(hash_file)

    change_file_list = []
    file_list = glob.glob(file_path + "/*." + file_type)
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

def push_to_github(change_file_list,name_list_path,hash_json_file):
    change_file_list.append(hash_json_file)
    change_file_list.append(name_list_path)
    for file in change_file_list:
        try:
            subprocess.call(f"git add {file}", shell=True)
        except:
            continue

    commit_message = 'git commit -m "Update configs"'
    subprocess.call(commit_message, shell=True)
    
    subprocess.call("git push", shell=True)

def gitpush_json(config_path,hash_path,name_list_path):
    change_file_list = hash_check(config_path,"json",hash_path)
    if len(change_file_list) > 0:
        push_to_github(change_file_list,name_list_path,hash_path)