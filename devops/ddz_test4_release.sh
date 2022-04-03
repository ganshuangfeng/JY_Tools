#!/bin/bash
#时间：2020/11/19
#peiyanfei
#功能：1、复制预发布到产品服务器 2、退出

#选项菜单

echo -e "\033[31m******************************\033[0m"
echo "*  num        command        *"
echo "*   1   cp test4 to release  *"
echo "*   2          quit          *"
echo -e "\033[31m******************************\033[0m"

while true; do
#获取键入值
	read -p "Enter a num option: " a
	while [ "$a" != '1' -a "$a" != '2' -o -z "$a" ]; do
		read -p "Enter a num option: " a 
	done

#键入值为对应值的执行动作
	case "$a" in
#键入值为1时，进入各节点主目录复制到本地再复制到产品服务器。
	1)
		scp -rp root@172.18.107.241:/home/skynet4/jy_data/* /root/skynet4/jy_data/ &> /dev/null
		scp -rp root@172.18.107.241:/home/skynet4/jy_gate/* /root/skynet4/jy_gate/ &> /dev/null
		scp -rp root@172.18.107.242:/home/skynet4/jy_game/* /root/skynet4/jy_game/ &> /dev/null
		scp -rp root@172.18.107.242:/home/skynet4/jy_tg/* /root/skynet4/jy_tg/ &> /dev/null
		rm -rf /root/skynet4/{jy_data,jy_gate,jy_game,jy_tg}/{logs,logs.bak}/*
		scp -rp /root/skynet4/jy_game/* root@172.18.107.233:/home/jy/skynet_test4/ &> /dev/null && if [ $? -eq 0 ];then echo "cp game to release success";else echo "cp game to release have error";fi
		scp -rp /root/skynet4/jy_gate/* root@172.18.107.234:/home/jy/skynet_test4/ &> /dev/null && if [ $? -eq 0 ];then echo "cp gate to release success";else echo "cp gate to release have error";fi
		scp -rp /root/skynet4/jy_data/* root@172.18.107.235:/home/jy/skynet_test4/ &> /dev/null && if [ $? -eq 0 ];then echo "cp data to release success";else echo "cp data to release have error";fi
		scp -rp /root/skynet4/jy_tg/* root@172.18.107.238:/home/jy/skynet_test4/ &> /dev/null && if [ $? -eq 0 ];then echo "cp tg to release success";else echo "cp tg to release have error";fi
		;;
#键入值为2时，退出
	2)
		echo "quit"
		exit 0
		;;
	esac
done
