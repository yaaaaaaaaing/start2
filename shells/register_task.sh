#!/bin/bash

echo "Content-type: text/plain"
echo ""

cd /var/www/start2/ || exit 1
# 读取 POST 数据
read INPUT_DATA

# 解析参数（client_email 和 check_type）
CLIENT_EMAIL=$(echo "$INPUT_DATA" | sed -n 's/.*client_email=\([^&]*\).*/\1/p' | sed 's/%40/@/g')
CHECK_TYPE=$(echo "$INPUT_DATA" | sed -n 's/.*check_type=\([^&]*\).*/\1/p')
DAYS=$(echo "$INPUT_DATA" | sed -n 's/.*days=\([^&]*\).*/\1/p')
TOKEN=$(echo "$INPUT_DATA" | sed -n 's/.*token=\([^&]*\).*/\1/p')

TARGET_TOKEN="tianjin-000"

# 校验 token
if [ "$TOKEN" != "$TARGET_TOKEN" ]; then
    echo "Error: Invalid token"
    exit 1
fi
    python3 /var/www/start2/register_check_trig.py -c "$CLIENT_EMAIL" -t "$CHECK_TYPE" -d "$DAYS"
    echo "successfully test"