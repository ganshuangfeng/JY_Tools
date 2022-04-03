#!/bin/sh
#
# Author: lyx
# Date: 2018/11/10
# Time: 10:52
# 说明： 拉代码
#
# mkdir ./skynet
# cp -f -r  ./skynet4/* ./skynet

set -e

source_dir=$1
branch_name=$2

# cur_path=$(pwd)

cd ${source_dir}
git reset --hard
git fetch
git checkout ${branch_name}
git pull

# cd ${cur_path}



