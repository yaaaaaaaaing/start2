# -*- coding: utf-8 -*-
from register_check_if import *
from send_receive_email import *
from init import *

def receive_text_parse(receive_text_list,token_register):
    register_check_dict = {}
    for receive_text in receive_text_list:
        if token_register in receive_text:
            receive_text_list = receive_text.split()
            for receive_text_ele in receive_text_list:
                if "@" in receive_text_ele and "." in receive_text_ele:
                    clinet_email = receive_text_ele
                    register_check_dict[clinet_email] = []
            for account_type in mapping_dict:
                if account_type in receive_text_list:
                    register_check_dict[clinet_email].append({"type":account_type,"days":30})
            if "only_check" in receive_text_list:
                register_check_dict[clinet_email] = []
                for account_type in mapping_dict:
                    if account_type in receive_text_list:
                        register_check_dict[clinet_email].append({"type":account_type,"days":0})
    return register_check_dict
                    
if __name__ == '__main__':
    database_branch = "develop"
    pull_database_from_github(config_path,database_branch)

    token_register = "tianjin-000"
    receive_text_list = receive_email()
    register_check_dict = receive_text_parse(receive_text_list,token_register)

    add_account_to_name_list(register_check_dict,name_list_path)
    update_client_expiration(register_check_dict,expiration_dict_path)
    updata_name_list(name_list_path,client_conf_path,hash_path)
    commit_message = "regenerate "
    for client_email in register_check_dict:
        add_account_to_codecheck_dict(client_email,client_conf_path,code_check_dict_path,mapping_dict)
        commit_message += "update config for " + client_email + " \n"

    for client_email in register_check_dict:
        send_specific_info(client_email,client_conf_path)

    commit_message = "update config for all client"
    gitpush_json(config_path,hash_path,name_list_path,commit_message)

    

