#!/bin/bash
#时间：2020/07/27
#peiyanfei
#功能：1、一键启动 2、一键停止 3、清理2天前的日志
#注意事项：1、运行脚本前需要主机相互SSH信任免密	2、目录需要提前存在
#选项菜单
echo -e "\033[31m************************************\033[0m"
echo "*          num        command      *"
echo "*   1    start aliyun_test_single  *"
echo "*   2    stop aliyun_test_single   *"
echo "*   3     clean log 1 days ago     *"
echo "*   4         git pull master      *"
echo "*   5               quit           *"
echo -e "\033[31m************************************\033[0m"
while true; do
#获取键入值
	read -p "Enter a num option: " a
	while [ "$a" != '1' -a "$a" != '2' -a "$a" != '3' -a "$a" != '4' -a "$a" != '5' -o -z "$a" ]; do
		read -p "Enter a num option: " a 
	done

#键入值为对应值的执行动作
	case "$a" in
#键入值为1时，进入各节点主目录并启动相关lua脚本。
	1)
		ssh root@172.18.124.191 "cd /home/jy/skynet/ && ./skynet game/launch/aliyun_test_single/single_config.lua;if [ $? -eq 0 ];then echo "start aliyun_test_single success";else echo "start aliyun_test_single error" && exit 2;fi" && curl 'https://oapi.dingtalk.com/robot/send?access_token=06ede20ac19dbbeaca47dd1642d906e2659a25d4adc86f50f9bd1bce5c746838' -H 'Content-Type: application/json' -d '{"msgtype": "text","text":{"content":"捕鱼预发布已重启完成"}}' &> /dev/null
		;;
#键入值为2时，进入各节点主目录，自动杀死服务端进程并且压缩log文件，并删除源文件。
	2)
		curl 'https://oapi.dingtalk.com/robot/send?access_token=06ede20ac19dbbeaca47dd1642d906e2659a25d4adc86f50f9bd1bce5c746838' -H 'Content-Type: application/json' -d '{"msgtype": "text","text":{"content":"捕鱼预发布已停止，将会重启"}}' && sleep 2
		ssh root@172.18.124.191 "cd /home/jy/skynet/logs && ps aux | grep "[g]ame/launch/aliyun_test_single" | awk '{print \$2}' | xargs kill -9 && tar -zcf `date +%Y%m%d%H%M`.tar.gz *.log && rm -rf *.log *.pid;if [ $? -eq 0 ];then echo "stop aliyun_test_single success";else echo "stop aliyun_test_single error" && exit 6;fi"
		;;
#键入值为3时，搜索超过1天的log压缩文件并删除。
	3)
		ssh root@172.18.124.191 "find /home/jy/skynet/logs/ -mtime +1 -name "*.tar.gz" -exec rm -rf {} \; && find /home/jy/skynet/logs/ -mtime +1 -name "*.txt" -exec rm -rf {} \; && find /home/jy/skynet/logs.bak/ -mtime +1 -name "*.log" -exec rm -rf {} \;;if [ $? -eq 0 ];then echo "clean aliyun_test_single_log success";else echo "clean aliyun_test_single_log error" && exit 10;fi"
		;;
#键入值为4时，拉取match_dev分支并部署
	4)
		cd /home/hlby/HuanLe_server && git reset --hard origin/master && git pull && scp -rp ./skynet/game/* root@172.18.124.191:/home/jy/skynet/game/ &> /dev/null && if [ $? -eq 0 ];then echo "pull master success";else echo "pull master error" && exit 14;fi
		;;
#键入值为5时，退出
	5)
		echo "quit"
		exit 0
		;;
	esac
done

