#!/bin/sh
#
# Author: lyx
# Date: 2018/11/10
# Time: 10:52
# 说明： 停服务
#
# mkdir ./skynet
# cp -f -r  ./skynet4/* ./skynet

set -e

root="/home/deploy_node/prepare/"

# 先停网关
ssh 172.18.107.235 "${root}"

# 备份旧版本


# 备份数据库