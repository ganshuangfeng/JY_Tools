# -*- coding: utf-8 -*- 
import os
import os.path
import xdrlib,sys
import types
import time

import glvar

# 源代码路径
glvar.source_dir = "/home/jyserver/deploy/JyQipai_server/"

# 中心、节点上的部署文件夹
glvar.center_deploy_dir = "/home/jyserver/deploy/"
glvar.node_deploy_dir = "/home/deploy/"

# 分支名字
glvar.branch_name = "DevOps_test"
# 启动配置名字
glvar.launch_name = "aliyun_prepare"


print("===============================")
print("1. 全新安装服务器!")
print("2. 更新服务器代码!")
print("===============================")
print("　　")

replay = input('输入部署类型(直接回车退出):')

if replay != "1" and replay != "2":
    os._exit(0)

cur_dir = os.getcwd()

print("正在拉取源代码...")
os.chdir(glvar.source_dir)
os.system("git reset --hard")
os.system("git fetch")
os.system("git checkout " + glvar.branch_name)
os.system("git reset --hard")


os.chdir(cur_dir)
    
