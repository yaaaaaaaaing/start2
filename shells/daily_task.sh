cd /var/www/start2/ || exit 1
python3 /var/www/start2/wechat_token_trigger.py --wechat_type "daily"
python3 /var/www/start2/expiration_check_trigger.py --expire_type "dailycheck"
