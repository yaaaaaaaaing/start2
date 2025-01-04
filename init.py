
hash_path = "./configuration/hash.json"
name_list_path = "./configuration/name_list.xlsx"
client_conf_path = "./configuration/client_info.json"
expiration_dict_path = "./configuration/expiration_info.json"

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
attachment_dict = {"vpn":"./attachment/netflix使用说明.pdf","nf":"./attachment/代理操作说明.pdf"}

mapping_dict = {
    "vpn account": {
        "client in name list": column_client_vpn_email,
        "expiration data in name list": column_serv_vpn_expiration,
        "attachment": "./attachment/netflix使用说明.pdf"
    },
    "nf account": {
        "client in name list": column_client_nf_email,
        "expiration data in name list": column_serv_nf_expiration,
        "attachment": "./attachment/代理操作说明.pdf"
    }
}