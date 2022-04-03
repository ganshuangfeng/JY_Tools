#!/bin/bash
#时间：2019/07/18
#peiyanfei
#功能：1、一键启动 2、一键停止 3、清理10天前的日志
#注意事项：1、运行脚本前需要主机相互SSH信任免密	2、目录需要提前存在

#远程主机是否在线
#for i in $(seq 2); do
#	ping -w 1 172.18.107.24$i &> /dev/null
#	if [ $? -ne 0 ]; then
#		echo "172.18.107.24$i no online" && exit 1
#	else echo "172.18.107.24$i is online"
#	fi
#done

#选项菜单

echo -e "\033[31m******************************\033[0m"
echo "*  num        command        *"
echo "*   1    start aliyun_test4  *"
echo "*   2    stop aliyun_test4   *"
echo "*   3   clean log 1 days ago *"
echo "*   4      pull match_dev    *"
echo "*   5           quit         *"
echo -e "\033[31m******************************\033[0m"

while true; do
#获取键入值
	read -p "Enter a num option: " a
	while [ "$a" != '1' -a "$a" != '2' -a "$a" != '3' -a "$a" != '4' -a "$a" != '5' -o -z "$a" ]; do
		read -p "Enter a num option: " a 
	done

#键入值为对应值的执行动作
	case "$a" in
#键入值为1时，进入各节点主目录并启动相关lua脚本，tg_config.lua在30秒后启动。
	1)
		ssh root@172.18.107.241 "cd /home/skynet4/jy_data && ./skynet game/launch/aliyun_test4/data_config.lua;if [ $? -eq 0 ];then echo "start data success";else echo "start data error" && exit 2;fi"
		ssh root@172.18.107.241 "cd /home/skynet4/jy_gate && ./skynet game/launch/aliyun_test4/gate_config.lua;if [ $? -eq 0 ];then echo "start gate success";else echo "start gate error" && exit 3;fi"
		ssh root@172.18.107.242 "cd /home/skynet4/jy_game && ./skynet game/launch/aliyun_test4/game_config.lua;if [ $? -eq 0 ];then echo "start game success";else echo "start game error" && exit 4;fi"
		ssh root@172.18.107.242 "cd /home/skynet4/jy_tg && sleep 20 && ./skynet game/launch/aliyun_test4/tg_config.lua;if [ $? -eq 0 ];then echo "start tg success";else echo "start tg error" && exit 5;fi" && if [ $? -eq 0 ];then curl 'https://oapi.dingtalk.com/robot/send?access_token=06ede20ac19dbbeaca47dd1642d906e2659a25d4adc86f50f9bd1bce5c746838' -H 'Content-Type: application/json' -d '{"msgtype": "text","text":{"content":"预发布已重启完成"}}' &> /dev/null;else exit 15;fi
		;;
#键入值为2时，进入各节点主目录，自动杀死服务端进程并且压缩log文件，并删除源文件。
	2)
		curl 'https://oapi.dingtalk.com/robot/send?access_token=06ede20ac19dbbeaca47dd1642d906e2659a25d4adc86f50f9bd1bce5c746838' -H 'Content-Type: application/json' -d '{"msgtype": "text","text":{"content":"预发布已停止，将会重启"}}' && sleep 2
		ssh root@172.18.107.241 "cd /home/skynet4/jy_data/logs && ps aux | grep "[g]ame/launch/aliyun_test4" | awk '{print \$2}' | xargs kill -9 && tar -zcf `date +%Y%m%d%H%M`.tar.gz *.log && rm -rf *.log *.pid;if [ $? -eq 0 ];then echo "stop data success";else echo "stop data error" && exit 6;fi"
		ssh root@172.18.107.241 "cd /home/skynet4/jy_gate/logs && tar -zcf `date +%Y%m%d%H%M`.tar.gz *.log && rm -rf *.log *.pid;if [ $? -eq 0 ];then echo "stop gate success";else echo "stop gate error" && exit 7;fi"
		ssh root@172.18.107.242 "cd /home/skynet4/jy_game/logs && ps aux | grep "[g]ame/launch/aliyun_test4" | awk '{print \$2}' | xargs kill -9 && tar -zcf `date +%Y%m%d%H%M`.tar.gz *.log && rm -rf *.log *.pid;if [ $? -eq 0 ];then echo "stop game success";else echo "stop game error" && exit 8;fi"
		ssh root@172.18.107.242 "cd /home/skynet4/jy_tg/logs && tar -zcf `date +%Y%m%d%H%M`.tar.gz *.log && rm -rf *.log *.pid;if [ $? -eq 0 ];then echo "stop tg success";else echo "stop tg error" && exit 9;fi"
		;;
#键入值为3时，搜索超过1天的log压缩文件并删除。
	3)
		ssh root@172.18.107.241 "find /home/skynet4/jy_data/logs -mtime +1 -name "*.tar.gz" -exec rm -rf {} \; && find /home/skynet4/jy_data/logs -mtime +1 -name "*.txt" -exec rm -rf {} \; && find /home/skynet4/jy_data/logs.bak -mtime +1 -name "*.log" -exec rm -rf {} \;;if [ $? -eq 0 ];then echo "clean data_log success";else echo "clean data_log error" && exit 10;fi"
		ssh root@172.18.107.241 "find /home/skynet4/jy_gate/logs -mtime +1 -name "*.tar.gz" -exec rm -rf {} \; && find /home/skynet4/jy_gate/logs -mtime +1 -name "*.txt" -exec rm -rf {} \; && find /home/skynet4/jy_gate/logs.bak -mtime +1 -name "*.log" -exec rm -rf {} \;;if [ $? -eq 0 ];then echo "clean gate_log success";else echo "clean gate_log error" && exit 11;fi"
		ssh root@172.18.107.242 "find /home/skynet4/jy_game/logs -mtime +1 -name "*.tar.gz" -exec rm -rf {} \; && find /home/skynet4/jy_game/logs -mtime +1 -name "*.txt" -exec rm -rf {} \; && find /home/skynet4/jy_game/logs.bak -mtime +1 -name "*.log" -exec rm -rf {} \;;if [ $? -eq 0 ];then echo "clean game_log success";else echo "clean game_log error" && exit 12;fi"
		ssh root@172.18.107.242 "find /home/skynet4/jy_tg/logs -mtime +1 -name "*.tar.gz" -exec rm -rf {} \; && find /home/skynet4/jy_tg/logs -mtime +1 -name "*.txt" -exec rm -rf {} \; && find /home/skynet4/jy_tg/logs.bak -mtime +1 -name "*.log" -exec rm -rf {} \;;if [ $? -eq 0 ];then echo "clean tg_log success";else echo "clean tg_log error" && exit 13;fi"
		;;
#键入值为4时，拉取match_dev分支并部署
	4)
		cd /home/JyQipai/JyQipai_server_dev/ && declare g=`date --date='Tuesday' +%Y%m%d` && git reset --hard origin/match_dev && git pull && if [ $? -eq 0 ];then echo "pull match_dev success";else echo "pull match_dev error" && exit 14;fi && git log --oneline | head -n 1 | awk '{print $1}' > /root/aliyun_release/ver_${g}.txt && scp -r /root/aliyun_release/ver_${g}.txt root@172.18.107.227:/root/aliyun_release/
		cd /home/JyQipai && bash cp4_game.sh &> /dev/null && if [ $? -eq 0 ];then echo "copy match_dev success";else echo "copy match_dev error" && exit 15;fi
		;;
#键入值为5时，退出
	5)
		echo "quit"
		exit 0
		;;
	esac
done
