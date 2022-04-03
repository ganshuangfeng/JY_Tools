#!/bin/bash
#时间：2020/11/19
#peiyanfei
#功能：1、复制预发布到产品服务器 2、退出

rm -rf /root/skynet4/test/*
#选项菜单

echo -e "\033[31m******************************\033[0m"
echo "*  num        command        *"
echo "*   1   cp test to release  *"
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
		scp -rp root@172.18.124.191:/home/jy/skynet/* /root/skynet4/test/ &> /dev/null && rm -rf /root/skynet4/test/{logs,logs.bak}/*
		scp -rp /root/skynet4/test/* root@172.18.124.184:/home/hlby_test/ &> /dev/null && if [ $? -eq 0 ];then echo "cp data gate to release success";else echo "cp data gate to release error" && exit 6;fi
		scp -rp /root/skynet4/test/* root@172.18.124.193:/home/hlby_test/ &> /dev/null && if [ $? -eq 0 ];then echo "cp game tg to release success";else echo "cp game tg to release error" && exit 7;fi
		;;
#键入值为2时，退出
	2)
		echo "quit"
		exit 0
		;;
	esac
done
