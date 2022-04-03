#!/bin/bash
#Date：2020/7/30
#Author：peiyanfei
#cpu=$(iostat -c | awk '{print \$1}' | sed -n '4p')
#usedisk=$(df -h | grep "/dev/vd" | awk '{print \$5}' | sort -r)
#dirdisk=$(df -h | grep "/dev/vd" | awk '{print \$6}' | sort -r)
#mem=$(free -g | awk '{print \$2}' | sed -n '2p')
#umem=$(free -g | awk '{print \$3}' | sed -n '2p')
ip=(172.18.107.247 172.18.107.231 172.18.107.235 172.18.107.233 172.18.107.234 172.18.107.237 172.18.107.238 172.18.107.232 172.18.107.244 172.18.107.243 172.18.107.245 172.18.107.246 47.115.32.238 119.23.224.240 120.24.26.204 8.129.168.130 120.24.35.62)

for i in ${ip[*]}; do
	case "$i" in
	${ip[0]})
		xzinfo=$(xzcpu=$(ssh root@$i "iostat -c | awk '{print \$1}' | sed -n '4p'") && xzusedisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5}' | sort -r | sed -n '1p'") && xzdirdisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5,\$6}' | sort -r | sed -n '1p' | awk '{print \$2}'") && xzmem=$(ssh root@$i "free -g | awk '{print \$2}' | sed -n '2p'") && xzumem=$(ssh root@$i "free -g | awk '{print \$3}' | sed -n '2p'") && echo -e "**生产环境-下载new系统信息**\n\nCPU使用率：$xzcpu%\n\n磁盘最大使用率：$xzusedisk $xzdirdisk\n\n总内存(GB)：$xzmem\n\n已使用(GB)：$xzumem")
#echo -e "$xzinfo"
		;;
	${ip[1]})
		sjbfinfo=$(sjbfcpu=$(ssh root@$i "iostat -c | awk '{print \$1}' | sed -n '4p'") && sjbfusedisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5}' | sort -r | sed -n '1p'") && sjbfdirdisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5,\$6}' | sort -r | sed -n '1p' | awk '{print \$2}'") && sjbfmem=$(ssh root@$i "free -g | awk '{print \$2}' | sed -n '2p'") && sjbfumem=$(ssh root@$i "free -g | awk '{print \$3}' | sed -n '2p'") && echo -e "**生产环境-数据备份系统信息**\n\nCPU使用率：$sjbfcpu%\n\n磁盘最大使用率：$sjbfusedisk $sjbfdirdisk\n\n总内存(GB)：$sjbfmem\n\n已使用(GB)：$sjbfumem")
#echo -e "$sjbfinfo"
		;;
	${ip[2]})
		yxsjinfo=$(yxsjcpu=$(ssh root@$i "iostat -c | awk '{print \$1}' | sed -n '4p'") && yxsjusedisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5}' | sort -r | sed -n '1p'") && yxsjdirdisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5,\$6}' | sort -r | sed -n '1p' | awk '{print \$2}'") && yxsjmem=$(ssh root@$i "free -g | awk '{print \$2}' | sed -n '2p'") && yxsjumem=$(ssh root@$i "free -g | awk '{print \$3}' | sed -n '2p'") && echo -e "**生产环境-游戏数据系统信息**\n\nCPU使用率：$yxsjcpu%\n\n磁盘最大使用率：$yxsjusedisk $yxsjdirdisk\n\n总内存(GB)：$yxsjmem\n\n已使用(GB)：$yxsjumem")
#echo -e "$yxsjinfo"
		;;
	${ip[3]})
		yxfwinfo=$(yxfwcpu=$(ssh root@$i "iostat -c | awk '{print \$1}' | sed -n '4p'") && yxfwusedisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5}' | sort -r | sed -n '1p'") && yxfwdirdisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5,\$6}' | sort -r | sed -n '1p' | awk '{print \$2}'") && yxfwmem=$(ssh root@$i "free -g | awk '{print \$2}' | sed -n '2p'") && yxfwumem=$(ssh root@$i "free -g | awk '{print \$3}' | sed -n '2p'") && echo -e "**生产环境-游戏服务系统信息**\n\nCPU使用率：$yxfwcpu%\n\n磁盘最大使用率：$yxfwusedisk $yxfwdirdisk\n\n总内存(GB)：$yxfwmem\n\n已使用(GB)：$yxfwumem")
#echo -e "$yxfwinfo"
		;;
	${ip[4]})
		yxwginfo=$(yxwgcpu=$(ssh root@$i "iostat -c | awk '{print \$1}' | sed -n '4p'") && yxwgusedisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5}' | sort -r | sed -n '1p'") && yxwgdirdisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5,\$6}' | sort -r | sed -n '1p' | awk '{print \$2}'") && yxwgmem=$(ssh root@$i "free -g | awk '{print \$2}' | sed -n '2p'") && yxwgumem=$(ssh root@$i "free -g | awk '{print \$3}' | sed -n '2p'") && echo -e "**生产环境-游戏网关系统信息**\n\nCPU使用率：$yxwgcpu%\n\n磁盘最大使用率：$yxwgusedisk $yxwgdirdisk\n\n总内存(GB)：$yxwgmem\n\n已使用(GB)：$yxwgumem")
#echo -e "$yxwginfo"
		;;
	${ip[5]})
		ywzcnewinfo=$(ywzcnewcpu=$(ssh root@$i "iostat -c | awk '{print \$1}' | sed -n '4p'") && ywzcnewusedisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5}' | sort -r | sed -n '1p'") && ywzcnewdirdisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5,\$6}' | sort -r | sed -n '1p' | awk '{print \$2}'") && ywzcnewmem=$(ssh root@$i "free -g | awk '{print \$2}' | sed -n '2p'") && ywzcnewumem=$(ssh root@$i "free -g | awk '{print \$3}' | sed -n '2p'") && echo -e "**生产环境-业务支持new系统信息**\n\nCPU使用率：$ywzcnewcpu%\n\n磁盘最大使用率：$ywzcnewusedisk $ywzcnewdirdisk\n\n总内存(GB)：$ywzcnewmem\n\n已使用(GB)：$ywzcnewumem")
#echo -e "$ywzcnewinfo"
		;;
	${ip[6]})
		yxtginfo=$(yxtgcpu=$(ssh root@$i "iostat -c | awk '{print \$1}' | sed -n '4p'") && yxtgusedisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5}' | sort -r | sed -n '1p'") && yxtgdirdisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5,\$6}' | sort -r | sed -n '1p' | awk '{print \$2}'") && yxtgmem=$(ssh root@$i "free -g | awk '{print \$2}' | sed -n '2p'") && yxtgumem=$(ssh root@$i "free -g | awk '{print \$3}' | sed -n '2p'") && echo -e "**生产环境-游戏托管系统信息**\n\nCPU使用率：$yxtgcpu%\n\n磁盘最大使用率：$yxtgusedisk $yxtgdirdisk\n\n总内存(GB)：$yxtgmem\n\n已使用(GB)：$yxtgumem")
#echo -e "$yxtginfo"
		;;
	${ip[7]})
		ywzcinfo=$(ywzccpu=$(ssh root@$i "iostat -c | awk '{print \$1}' | sed -n '4p'") && ywzcusedisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5}' | sort -r | sed -n '1p'") && ywzcdirdisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5,\$6}' | sort -r | sed -n '1p' | awk '{print \$2}'") && ywzcmem=$(ssh root@$i "free -g | awk '{print \$2}' | sed -n '2p'") && ywzcumem=$(ssh root@$i "free -g | awk '{print \$3}' | sed -n '2p'") && echo -e "**生产环境-业务支持系统信息**\n\nCPU使用率：$ywzccpu%\n\n磁盘最大使用率：$ywzcusedisk $ywzcdirdisk\n\n总内存(GB)：$ywzcmem\n\n已使用(GB)：$ywzcumem")
#echo -e "$ywzcinfo"
		;;
	${ip[8]})
		bbinfo=$(bbcpu=$(ssh root@$i "iostat -c | awk '{print \$1}' | sed -n '4p'") && bbusedisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5}' | sort -r | sed -n '1p'") && bbdirdisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5,\$6}' | sort -r | sed -n '1p' | awk '{print \$2}'") && bbmem=$(ssh root@$i "free -g | awk '{print \$2}' | sed -n '2p'") && bbumem=$(ssh root@$i "free -g | awk '{print \$3}' | sed -n '2p'") && echo -e "**生产环境-转发-版本信息系统信息**\n\nCPU使用率：$bbcpu%\n\n磁盘最大使用率：$bbusedisk $bbdirdisk\n\n总内存(GB)：$bbmem\n\n已使用(GB)：$bbumem")
#echo -e "$bbinfo"
		;;
	${ip[9]})
		zfyxfwinfo=$(zfyxfwcpu=$(ssh root@$i "iostat -c | awk '{print \$1}' | sed -n '4p'") && zfyxfwusedisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5}' | sort -r | sed -n '1p'") && zfyxfwdirdisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5,\$6}' | sort -r | sed -n '1p' | awk '{print \$2}'") && zfyxfwmem=$(ssh root@$i "free -g | awk '{print \$2}' | sed -n '2p'") && zfyxfwumem=$(ssh root@$i "free -g | awk '{print \$3}' | sed -n '2p'") && echo -e "**生产环境-转发-游戏服务系统信息**\n\nCPU使用率：$zfyxfwcpu%\n\n磁盘最大使用率：$zfyxfwusedisk $zfyxfwdirdisk\n\n总内存(GB)：$zfyxfwmem\n\n已使用(GB)：$zfyxfwumem")
#echo -e "$zfyxfwinfo"
		;;
	${ip[10]})
		yxfwvipinfo=$(yxfwvipcpu=$(ssh root@$i "iostat -c | awk '{print \$1}' | sed -n '4p'") && yxfwvipusedisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5}' | sort -r | sed -n '1p'") && yxfwvipdirdisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5,\$6}' | sort -r | sed -n '1p' | awk '{print \$2}'") && yxfwvipmem=$(ssh root@$i "free -g | awk '{print \$2}' | sed -n '2p'") && yxfwvipumem=$(ssh root@$i "free -g | awk '{print \$3}' | sed -n '2p'") && echo -e "**生产环境-转发-游戏服务VIP系统信息**\n\nCPU使用率：$yxfwvipcpu%\n\n磁盘最大使用率：$yxfwvipusedisk $yxfwvipdirdisk\n\n总内存(GB)：$yxfwvipmem\n\n已使用(GB)：$yxfwvipumem")
#echo -e "$yxfwvipinfo"
		;;
	${ip[11]})
		sjckinfo=$(sjckcpu=$(ssh root@$i "iostat -c | awk '{print \$1}' | sed -n '4p'") && sjckusedisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5}' | sort -r | sed -n '1p'") && sjckdirdisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5,\$6}' | sort -r | sed -n '1p' | awk '{print \$2}'") && sjckmem=$(ssh root@$i "free -g | awk '{print \$2}' | sed -n '2p'") && sjckumem=$(ssh root@$i "free -g | awk '{print \$3}' | sed -n '2p'") && echo -e "**生产环境-数据仓库系统信息**\n\nCPU使用率：$sjckcpu%\n\n磁盘最大使用率：$sjckusedisk $sjckdirdisk\n\n总内存(GB)：$sjckmem\n\n已使用(GB)：$sjckumem")
#echo -e "$sjckinfo"
		;;
#欢乐天天捕鱼
	${ip[12]})
		hlbydginfo=$(hlbydgcpu=$(ssh root@$i "iostat -c | awk '{print \$1}' | sed -n '4p'") && hlbydgusedisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5}' | sort -r | sed -n '1p'") && hlbydgdirdisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5,\$6}' | sort -r | sed -n '1p' | awk '{print \$2}'") && hlbydgmem=$(ssh root@$i "free -g | awk '{print \$2}' | sed -n '2p'") && hlbydgumem=$(ssh root@$i "free -g | awk '{print \$3}' | sed -n '2p'") && echo -e "**生产环境-欢乐捕鱼数据和网关系统信息**\n\nCPU使用率：$hlbydgcpu%\n\n磁盘最大使用率：$hlbydgusedisk $hlbydgdirdisk\n\n总内存(GB)：$hlbydgmem\n\n已使用(GB)：$hlbydgumem")
#echo -e "$hlbydginfo"
		;;
	${ip[13]})
		hlbysjbfinfo=$(hlbysjbfcpu=$(ssh root@$i "iostat -c | awk '{print \$1}' | sed -n '4p'") && hlbysjbfusedisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5}' | sort | sed -n '1p'") && hlbysjbfdirdisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5,\$6}' | sort -r | sed -n '1p' | awk '{print \$2}'") && hlbysjbfmem=$(ssh root@$i "free -g | awk '{print \$2}' | sed -n '2p'") && hlbysjbfumem=$(ssh root@$i "free -g | awk '{print \$3}' | sed -n '2p'") && echo -e "**生产环境-欢乐捕鱼数据备份系统信息**\n\nCPU使用率：$hlbysjbfcpu%\n\n磁盘最大使用率：$hlbysjbfusedisk $hlbysjbfdirdisk\n\n总内存(GB)：$hlbysjbfmem\n\n已使用(GB)：$hlbysjbfumem")
#echo -e "$hlbysjbfinfo"
		;;
	${ip[14]})
		hlbygtinfo=$(hlbygtcpu=$(ssh root@$i "iostat -c | awk '{print \$1}' | sed -n '4p'") && hlbygtusedisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5}' | sort -r | sed -n '1p'") && hlbygtdirdisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5,\$6}' | sort -r | sed -n '1p' | awk '{print \$2}'") && hlbygtmem=$(ssh root@$i "free -g | awk '{print \$2}' | sed -n '2p'") && hlbygtumem=$(ssh root@$i "free -g | awk '{print \$3}' | sed -n '2p'") && echo -e "**生产环境-欢乐捕鱼游戏和托管系统信息**\n\nCPU使用率：$hlbygtcpu%\n\n磁盘最大使用率：$hlbygtusedisk $hlbygtdirdisk\n\n总内存(GB)：$hlbygtmem\n\n已使用(GB)：$hlbygtumem")
#echo -e "$hlbygtinfo"
		;;
	${ip[15]})
		hlbyywzcinfo=$(hlbyywzccpu=$(ssh root@$i "iostat -c | awk '{print \$1}' | sed -n '4p'") && hlbyywzcusedisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5}' | sort -r | sed -n '1p'") && hlbyywzcdirdisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5,\$6}' | sort -r | sed -n '1p' | awk '{print \$2}'") && hlbyywzcmem=$(ssh root@$i "free -g | awk '{print \$2}' | sed -n '2p'") && hlbyywzcumem=$(ssh root@$i "free -g | awk '{print \$3}' | sed -n '2p'") && echo -e "**生产环境-欢乐捕鱼业务支持系统信息**\n\nCPU使用率：$hlbyywzccpu%\n\n磁盘最大使用率：$hlbyywzcusedisk $hlbyywzcdirdisk\n\n总内存(GB)：$hlbyywzcmem\n\n已使用(GB)：$hlbyywzcumem")
#echo -e "$hlbyywzcinfo"
		;;
	${ip[16]})
		hlbysjckinfo=$(hlbysjckcpu=$(ssh root@$i "iostat -c | awk '{print \$1}' | sed -n '4p'") && hlbysjckusedisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5}' | sort -r | sed -n '1p'") && hlbysjckdirdisk=$(ssh root@$i "df -h | grep "/dev/vd" | awk '{print \$5,\$6}' | sort -r | sed -n '1p' | awk '{print \$2}'") && hlbysjckmem=$(ssh root@$i "free -g | awk '{print \$2}' | sed -n '2p'") && hlbysjckumem=$(ssh root@$i "free -g | awk '{print \$3}' | sed -n '2p'") && echo -e "**生产环境-欢乐捕鱼数据仓库系统信息**\n\nCPU使用率：$hlbysjckcpu%\n\n磁盘最大使用率：$hlbysjckusedisk $hlbysjckdirdisk\n\n总内存(GB)：$hlbysjckmem\n\n已使用(GB)：$hlbysjckumem")
#echo -e "$hlbysjckinfo"
		;;
	esac
done

curl 'https://oapi.dingtalk.com/robot/send?access_token=06ede20ac19dbbeaca47dd1642d906e2659a25d4adc86f50f9bd1bce5c746838' -H 'Content-Type:application/json' -d "{'msgtype':'markdown','markdown':{'title':'生产环境检查','text':'<font color=#FF0000 size=3>★★★【鲸鱼斗地主】★★★</font>\n\n${xzinfo}\n\n${sjbfinfo}\n\n${yxsjinfo}\n\n${yxfwinfo}\n\n${yxwginfo}\n\n${ywzcnewinfo}\n\n${yxtginfo}\n\n${ywzcinfo}\n\n${bbinfo}\n\n${zfyxfwinfo}\n\n${yxfwvipinfo}\n\n${sjckinfo}\n\n<font color=#FF0000 size=3>※※※【欢乐天天捕鱼】※※※</font>\n\n${hlbydginfo}\n\n${hlbysjbfinfo}\n\n${hlbygtinfo}\n\n${hlbyywzcinfo}\n\n${hlbysjckinfo}\n\n @13880350313'},'at':{'atMobiles':['13880350313'],'isAtAll':false}}"























