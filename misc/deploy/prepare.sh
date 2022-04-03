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

python ./center/prepare.py
