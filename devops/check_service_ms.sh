#!/bin/bash
#Date:2020/7/2
#Author:peiyf

services=(jy_huawei aliyun_test_wzddz jy_check hlby_vivo_tishen ti_shen_fu yy_single_test)
service=()
service[0]=$(ssh root@172.18.107.241 "ps -ef" | grep jy_huawei/single_config.lua$ | awk '{print $9}' | awk -F"/" '{print $3}')
service[1]=$(ssh root@172.18.107.241 "ps -ef" | grep aliyun_test_wzddz/single_config.lua$ | awk '{print $9}' | awk -F"/" '{print $3}')
service[2]=$(ssh root@172.18.107.227 "ps -ef" | grep jy_check/single_config.lua$ | awk '{print $9}' | awk -F"/" '{print $3}')
service[3]=$(ssh root@172.18.107.249 "ps -ef" | grep hlby_vivo_tishen/single_config.lua$ | awk '{print $9}' | awk -F"/" '{print $3}')
service[4]=$(ssh root@8.129.217.169 "ps -ef" | grep ti_shen_fu/single_config.lua$ | awk '{print $9}' | awk -F"/" '{print $3}')
service[5]=$(ssh root@172.18.107.248 "ps -ef" | grep yy_single_test/single_config.lua$ | awk '{print $9}' | awk -F"/" '{print $3}')

if [ "${service[0]}" != "${services[0]}" ]; then
	curl 'https://oapi.dingtalk.com/robot/send?access_token=06ede20ac19dbbeaca47dd1642d906e2659a25d4adc86f50f9bd1bce5c746838' -H 'Content-Type: application/json' -d "{'msgtype': 'markdown','markdown':{'title':'有服务未运行','text':'<font color=#FF0000 size=3>华为彩云麻将：未运行</font>'}}"
elif [ "${service[1]}" != "${services[1]}" ]; then
	curl 'https://oapi.dingtalk.com/robot/send?access_token=06ede20ac19dbbeaca47dd1642d906e2659a25d4adc86f50f9bd1bce5c746838' -H 'Content-Type: application/json' -d "{'msgtype': 'markdown','markdown':{'title':'有服务未运行','text':'<font color=#FF0000 size=3>网赚斗地主：未运行</font>'}}"
elif [ "${service[2]}" != "${services[2]}" ]; then
	curl 'https://oapi.dingtalk.com/robot/send?access_token=06ede20ac19dbbeaca47dd1642d906e2659a25d4adc86f50f9bd1bce5c746838' -H 'Content-Type: application/json' -d "{'msgtype': 'markdown','markdown':{'title':'有服务未运行','text':'<font color=#FF0000 size=3>彩云麻将/五子棋：未运行</font>'}}"
elif [ "${service[3]}" != "${services[3]}" ]; then
	curl 'https://oapi.dingtalk.com/robot/send?access_token=06ede20ac19dbbeaca47dd1642d906e2659a25d4adc86f50f9bd1bce5c746838' -H 'Content-Type: application/json' -d "{'msgtype': 'markdown','markdown':{'title':'有服务未运行','text':'<font color=#FF0000 size=3>欢乐捕鱼vivo_提审：未运行</font>'}}"
elif [ "${service[4]}" != "${services[4]}" ]; then
	curl 'https://oapi.dingtalk.com/robot/send?access_token=06ede20ac19dbbeaca47dd1642d906e2659a25d4adc86f50f9bd1bce5c746838' -H 'Content-Type: application/json' -d "{'msgtype': 'markdown','markdown':{'title':'有服务未运行','text':'<font color=#FF0000 size=3>苹果提审：未运行</font>'}}"
elif [ "${service[5]}" != "${services[5]}" ]; then
	curl 'https://oapi.dingtalk.com/robot/send?access_token=06ede20ac19dbbeaca47dd1642d906e2659a25d4adc86f50f9bd1bce5c746838' -H 'Content-Type: application/json' -d "{'msgtype': 'markdown','markdown':{'title':'有服务未运行','text':'<font color=#FF0000 size=3>小米提审：未运行</font>'}}"
fi
