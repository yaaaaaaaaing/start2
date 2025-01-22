# -*- coding: utf-8 -*-
config_path = "./configuration"
hash_path = "./configuration/hash.json"
name_list_path = "./configuration/name_list.xlsx"
client_conf_path = "./configuration/client_info.json"
expiration_dict_path = "./configuration/expiration_info.json"
code_check_dict_path = "./configuration/code_check_info.json"

num_max_slots = 5
column_serv_email = 1
column_serv_email_pw = 2
column_serv_nf_pw = 3
column_serv_nf_expiration = 4
column_serv_vpn_pw = 5
column_serv_vpn_expiration = 6
column_client_vpn_email = 7
column_client_nf_pin = 8
column_client_nf_email = 9

release_email_dict = {"output client infos":["serv_vpn_url","serv_nf_email","serv_nf_pin"],
                      "attchment_mapping":{"serv_vpn_url":"./attachment/vpn_guideline.pdf",
                                            "serv_nf_email":"./attachment/netflix_guideline.pdf"}}

mapping_dict = {
    "vpn_account": {
        "client in name list": column_client_vpn_email,
        "expiration data in name list": column_serv_vpn_expiration,
        "pin in name list": None,
        "attachment": "./attachment/netflix使用说明.pdf",
        "server email tag in name list": "serv_vpn_email",
        "server email pw tag in name list": "serv_vpn_email_pw",
        "tag": "vpn"
    },
    "nf_account": {
        "client in name list": column_client_nf_email,
        "expiration data in name list": column_serv_nf_expiration,
        "pin in name list": column_client_nf_pin,
        "attachment": "./attachment/代理操作说明.pdf",
        "server email tag in name list": "serv_nf_email",
        "server email pw tag in name list": "serv_nf_email_pw",
        "tag": "Netflix"
    }
}

server_email = "niustaat@gmail.com"