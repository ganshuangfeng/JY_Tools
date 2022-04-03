#!/bin/sh
#
# Author: lyx
# Date: 2018/11/10
# Time: 10:52
# 说明： 部署 最新代码到 预发布服务器
#
# mkdir ./skynet
# cp -f -r  ./skynet4/* ./skynet

set -e

# 

# 源代码路径
export source_dir="/home/jyserver/deploy/JyQipai_server/"

# 中心、节点上的部署文件夹
export center_deploy_dir="/home/jyserver/deploy/"
export node_deploy_dir="/home/deploy/"

# 分支名字
export branch_name="DevOps_test"
# 启动配置名字
export launch_name="aliyun_prepare"

echo "==============================="
echo "1. 全新安装服务器!"
echo "2. 更新服务器代码!"
echo "==============================="
echo "　　"
read -p "输入部署类型(直接回车退出):" replay

if [ "${replay}"x != "1"x ] && [ "${replay}"x != "2"x ]; then
    exit 1
fi

echo "正在拉取源代码..."
./center/pull_source.sh
echo "完成."
echo " "

echo "正在关闭服务..."
./center/stop_r_service.sh
echo "完成."
echo " "

# 备份
if [ "${replay}"x == "1"x ]; then

    echo "正在备份当前数据..."
    ./center/backup_r_service.sh
    echo "完成."
    echo " "

fi

echo "正在启动服务..."
./center/start_r_service.sh
echo "完成."


