#!/bin/bash
#Date:2020/06/08
#Author:peiyanfei
echo -e "\033[31m******************************\033[0m"
echo "*  num        command        *"
echo "*   1   mv test huanle_buyu  *"
echo "*   2    start huanle_buyu   *"
echo "*   3           quit         *"
echo -e "\033[31m******************************\033[0m"

while true; do
#获取键入值
	read -p "Enter a num option: " a
	while [ "$a" != '1' -a "$a" != '2' -a "$a" != '3' -o -z "$a" ]; do
		read -p "Enter a num option: " a 
	done

#键入值为对应值的执行动作
	case "$a" in
#键入值为1时，重命名欢乐捕鱼。
	1)
		ssh root@172.18.124.184 "cd /home/ && mv hlby_data hlby_data_$(date +%Y%m%d%H%M) && cp -r hlby_test hlby_data && mv hlby_gate hlby_gate_$(date +%Y%m%d%H%M) && mv hlby_test hlby_gate && mkdir hlby_test" && if [ $? -eq 0 ];then echo "mv data gate name success";else echo "mv data gate name error" && exit 6;fi
		ssh root@172.18.124.193 "cd /home/ && mv hlby_game hlby_game_$(date +%Y%m%d%H%M) && cp -r hlby_test hlby_game && mv hlby_tg hlby_tg_$(date +%Y%m%d%H%M) && mv hlby_test hlby_tg && mkdir hlby_test" && if [ $? -eq 0 ];then echo "mv game tg name success";else echo "mv game tg name error" && exit 7;fi
		;;
#键入值为2时，启动欢乐捕鱼进程。
	2)
		ssh root@172.18.124.184 "cd /home/hlby_data/ && ./skynet game/launch/aliyun_release/data_config.lua && cd /home/hlby_gate/ && ./skynet game/launch/aliyun_release/gate_config.lua"
		ssh root@172.18.124.193 "cd /home/hlby_game/ && ./skynet game/launch/aliyun_release/game_config.lua && sleep 20 && cd /home/hlby_tg/ && ./skynet game/launch/aliyun_release/tg_config.lua"
		curl 'https://oapi.dingtalk.com/robot/send?access_token=06ede20ac19dbbeaca47dd1642d906e2659a25d4adc86f50f9bd1bce5c746838' -H 'Content-Type: application/json' -d '{"msgtype": "text","text":{"content":"欢乐捕鱼已启动完成"}}' &> /dev/null
		;;

#键入值为3时，退出
	3)
		echo "quit"
		exit 0
		;;
	esac
done
