#!/bin/bash
#Date:2020/7/2
#Author:peiyf
services=(jy_huawei aliyun_test_wzddz jy_check hlby_vivo_tishen ti_shen_fu yy_single_test)
service=()
tz=()
service[0]=$(ssh root@172.18.107.241 "ps -ef" | grep jy_huawei/single_config.lua$ | awk '{print $9}' | awk -F"/" '{print $3}')
service[1]=$(ssh root@172.18.107.241 "ps -ef" | grep aliyun_test_wzddz/single_config.lua$ | awk '{print $9}' | awk -F"/" '{print $3}')
service[2]=$(ssh root@172.18.107.227 "ps -ef" | grep jy_check/single_config.lua$ | awk '{print $9}' | awk -F"/" '{print $3}')
service[3]=$(ssh root@172.18.107.249 "ps -ef" | grep hlby_vivo_tishen/single_config.lua$ | awk '{print $9}' | awk -F"/" '{print $3}')
service[4]=$(ssh root@8.129.217.169 "ps -ef" | grep ti_shen_fu/single_config.lua$ | awk '{print $9}' | awk -F"/" '{print $3}')
service[5]=$(ssh root@172.18.107.248 "ps -ef" | grep yy_single_test/single_config.lua$ | awk '{print $9}' | awk -F"/" '{print $3}')

if [ "${service[0]}" == "${services[0]}" ]; then
	tz[0]="华为彩云麻将：正在运行"
else tz[0]="华为彩云麻将：未运行"
fi
if [ "${service[1]}" == "${services[1]}" ]; then
	tz[1]="网赚斗地主：正在运行"
else tz[1]="网赚斗地主：未运行"
fi
if [ "${service[2]}" == "${services[2]}" ]; then
	tz[2]="彩云麻将/五子棋：正在运行"
else tz[2]="彩云麻将/五子棋：未运行"
fi
if [ "${service[3]}" == "${service[3]}" ]; then
	tz[3]="欢乐捕鱼vivo_提审：正在运行"
else tz[3]="欢乐捕鱼vivo_提审：未运行"
fi
if [ "${service[4]}" == "${services[4]}" ]; then
	tz[4]="苹果提审：正在运行"
else tz[4]="苹果提审：未运行"
fi
if [ "${service[5]}" == "${services[5]}" ]; then
	tz[5]="小米提审：正在运行"
else tz[5]="小米提审：未运行"
fi

#echo -e "${tz[0]}\n${tz[1]}\n${tz[2]}\n${tz[3]}\n"
curl 'https://oapi.dingtalk.com/robot/send?access_token=06ede20ac19dbbeaca47dd1642d906e2659a25d4adc86f50f9bd1bce5c746838' -H 'Content-Type: application/json' -d "{'msgtype': 'text','text':{'content':'${tz[0]}\n${tz[1]}\n${tz[2]}\n${tz[3]}\n${tz[4]}\n${tz[5]}'}}"
