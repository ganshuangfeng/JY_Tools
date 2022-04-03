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

ssh 172.18.107.234 "${node_deploy_dir}tools/stop_service.sh ${launch_name}"
ssh 172.18.107.233 "${node_deploy_dir}tools/stop_service.sh ${launch_name}"
ssh 172.18.107.235 "${node_deploy_dir}tools/stop_service.sh ${launch_name}"
