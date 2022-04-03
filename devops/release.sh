#!/bin/bash
#时间：2019/07/22
#peiyanfei
#功能：1、拷贝预发布服务端到产品端 2、一键部署启动
#注意事项：1、运行脚本前需要主机相互SSH信任免密	2、目录需要提前存在

rm -rf /root/skynet4/{jy_data,jy_gate,jy_game,jy_tg}/*

#选项菜单
cat << end
******************************
*  num        command        *
*   1     mv test4 to skynet *
*   2    start aliyun server *
*   3           quit         *
******************************
end

while true; do
#获取键入值
	read -p "Enter a num option: " a
	while [ "$a" != '1' -a "$a" != '2' -a "$a" != '3' -o -z "$a" ]; do
		read -p "Enter a num option: " a 
	done

#键入值为对应值的执行动作
	case "$a" in
#键入值为1时，进入各节点重命名目录
	1)
		ssh root@172.18.107.233 "cd /home/jy && mv skynet skynet_$(date +%Y%m%d%H%M) && mv skynet_test4 skynet && mkdir skynet_test4" && if [ $? -eq 0 ];then echo "mv gamename success";else echo "mv gamename have error";fi
		ssh root@172.18.107.234 "cd /home/jy && mv skynet skynet_$(date +%Y%m%d%H%M) && mv skynet_test4 skynet && mkdir skynet_test4" && if [ $? -eq 0 ];then echo "mv gatename success";else echo "mv gatename have error";fi
		ssh root@172.18.107.235 "cd /home/jy && mv skynet skynet_$(date +%Y%m%d%H%M) && mv skynet_test4 skynet && mkdir skynet_test4" && if [ $? -eq 0 ];then echo "mv dataname success";else echo "mv dataname have error";fi
		ssh root@172.18.107.238 "cd /home/jy && mv skynet skynet_$(date +%Y%m%d%H%M) && mv skynet_test4 skynet && mkdir skynet_test4" && if [ $? -eq 0 ];then echo "mv tgname success";else echo "mv tgname have error";fi
		;;
#键入值为2时，进入各节点主目录并启动相关lua脚本，tg_config.lua在120秒后启动。
	2)
		ssh root@172.18.107.233 "cd /home/jy/skynet && ./skynet game/launch/aliyun_release/game_config.lua;if [ $? -eq 0 ];then echo "start game success";else echo "start game error" && exit 2;fi"
		ssh root@172.18.107.234 "cd /home/jy/skynet && ./skynet game/launch/aliyun_release/gate_config.lua;if [ $? -eq 0 ];then echo "start gate success";else echo "start gate error" && exit 3;fi"
		ssh root@172.18.107.235 "cd /home/jy/skynet && ./skynet game/launch/aliyun_release/data_config.lua;if [ $? -eq 0 ];then echo "start data success";else echo "start data error" && exit 4;fi"
		#sleep 80 && echo "please start tg crontab"
		#ssh root@172.18.107.238 "cd /home/jy/skynet && sleep 300 && ./skynet game/launch/aliyun_release/tg_config.lua;if [ $? -eq 0 ];then echo "start tg success";else echo "start tg error" && exit 5;fi"
		;;

#键入值为3时，退出
	3)
		echo "quit"
		exit 0
		;;
	esac
done
