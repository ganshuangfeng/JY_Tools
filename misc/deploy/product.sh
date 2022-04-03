#!/bin/sh
#
# Author: lyx
# Date: 2018/11/10
# Time: 10:52
# 说明： 部署 预发布 服务器 到正式服务器
#
# mkdir ./skynet
# cp -f -r  ./skynet4/* ./skynet

set -e

export launch_name="aliyun_product"

export node_deploy_dir="/home/deploy/product"

echo "==============================="
echo "1. 全新安装服务器!"
echo "2. 更新服务器代码!"
echo "==============================="
echo "　　"
read -p "输入部署类型(直接回车退出):" replay

if [ "${replay}"x != "1"x ] && [ "${replay}"x != "2"x ]; then
    exit 1
fi
