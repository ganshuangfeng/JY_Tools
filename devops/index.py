#!/usr/bin/python3.5
# -*- coding:utf-8 -*-
# Date:2020/11/18
# Author:peiyanfei

import base64
import hashlib
import hmac
import json
import time
import os
import requests
from flask import Flask, request

app = Flask(__name__)
webhook = 'https://oapi.dingtalk.com/robot/send?access_token' \
          '=3d581ab9a4dcc4ef0f1aedc2ecf8c5b228239ac5a304caa874b96d6eb87aeb47 '
# webhook = 'https://oapi.dingtalk.com/robot/send?access_token' \
#          '=f47159af0a5ddd57570510431e36f6aa3f3969a4bb1775bc596eb84453653966 '
headers = {"Content-Type": "application/json", "Charset": "UTF-8"}

# 拥有权限人员
adminname = ('裴燕飞', '魏世顺', '杨洋', '竟娱互动--隆元线')


class Get_Data(object):
    def __init__(self, post_data):
        # post信息
        self.post_user = post_data.get("senderNick").strip()
        self.post_time = request.headers["Timestamp"].lstrip()
        self.post_sign = request.headers["Sign"].lstrip()
        self.post_mes = post_data.get("text").get('content').strip()
        # 钉钉校验
        self.timestamp = round(time.time() * 1000)
        self.app_secret = 'cP-Tmpc058GrqY1CDf3Pkfwfo8Lay5vISUA3xkuoz1IyqQcfYI8EKr88DyqsD8V9'
        self.app_secret_enc = self.app_secret.encode('utf-8')
        self.string_to_sign = '{}\n{}'.format(self.post_time, self.app_secret)
        self.string_to_sign_enc = self.string_to_sign.encode('utf-8')
        self.hmac_code = hmac.new(self.app_secret_enc, self.string_to_sign_enc, digestmod=hashlib.sha256).digest()
        self.sign = base64.b64encode(self.hmac_code).decode('utf-8')


def messge(mes):
    messge = {
        "msgtype": "text",
        "text": {
            "content": mes
        },
        "at": {
            "isAtAll": False
        }
    }
    return messge


@app.route('/', methods=['POST'])
def index():
    post_data = request.get_data().decode('utf-8')
    post_data = json.loads(post_data)
    data = Get_Data(post_data)
    if abs(int(data.post_time) - int(data.timestamp)) < 3600000 and data.post_sign == data.sign:
        # 鲸鱼斗地主
        if data.post_user in adminname and data.post_mes == '1':
            mes = "@%s\n正在拉取并拷贝match_dev" % data.post_user
            requests.post(url=webhook, json=messge(mes), headers=headers)
            with os.popen('cd /home/JyQipai/JyQipai_server_dev && git reset --hard origin/match_dev && git '
                          'pull && cd /home/JyQipai/ && ./cp4_game.sh && if [ '
                          '$? -eq 0 ];then echo "success";else echo "error";fi') as p:
                ddz_git_pull = p.read()
            with os.popen('cd /home/JyQipai/JyQipai_server_dev && git rev-parse --short HEAD') as p:
                git_hash = p.read()
            with os.popen('ssh root@172.18.107.241 "cd /home/skynet4/jy_data/ && ./kill.sh '
                          'aliyun_test4 && cd logs/ && rm -rf *.log *.pid" && if [ $? -eq 0 ];then echo '
                          '"success";else echo "error";fi') as p:
                test4_stop_dg = p.read()
            with os.popen('ssh root@172.18.107.242 "cd /home/skynet4/jy_game/ && ./kill.sh '
                          'aliyun_test4 && cd logs/ && rm -rf *.log *.pid" && if [ $? -eq 0 ];then echo '
                          '"success";else echo "error";fi') as p:
                test4_stop_gt = p.read()
            if 'success' in ddz_git_pull and 'success' in test4_stop_dg and 'success' in test4_stop_gt:
                mes = "@%s\n鲸鱼斗地主预发布已停止，将立即启动" % data.post_user
                requests.post(url=webhook, json=messge(mes), headers=headers)
                with os.popen('ssh root@172.18.107.241 "cd /home/skynet4/jy_data && ./skynet '
                              'game/launch/aliyun_test4/data_config.lua && cd /home/skynet4/jy_gate && '
                              './skynet game/launch/aliyun_test4/gate_config.lua" && if [ $? -eq 0 ];then '
                              'echo "success";else echo "error";fi') as p:
                    test4_start_dg = p.read()
                with os.popen('ssh root@172.18.107.242 "cd /home/skynet4/jy_game && ./skynet '
                              'game/launch/aliyun_test4/game_config.lua && cd /home/skynet4/jy_tg && '
                              'sleep 20 && ./skynet game/launch/aliyun_test4/tg_config.lua" && if [ $? '
                              '-eq 0 ];then echo "success";else echo "error";fi') as p:
                    test4_start_gt = p.read()
                if 'success' in test4_start_dg and 'success' in test4_start_gt:
                    mes = "@%s\n鲸鱼斗地主预发布已启动完成\n当前分支版本为:%s" % (data.post_user, git_hash)
                    requests.post(url=webhook, json=messge(mes), headers=headers)
                    return ''
                else:
                    mes = "@%s\n鲸鱼斗地主预发布启动失败" % data.post_user
                    requests.post(url=webhook, json=messge(mes), headers=headers)
                    return ''
            else:
                mes = "@%s\n鲸鱼斗地主预发布停止失败" % data.post_user
                requests.post(url=webhook, json=messge(mes), headers=headers)
                return ''
        # 欢乐天天捕鱼
        elif data.post_user in adminname and data.post_mes == '2':
            mes = "@%s\n正在拉取并拷贝master" % data.post_user
            requests.post(url=webhook, json=messge(mes), headers=headers)
            with os.popen('ssh root@120.76.174.183 "cd /home/hlby/HuanLe_server && git reset --hard '
                          'origin/master && git pull && scp -rp ./skynet/game/* '
                          'root@172.18.124.191:/home/jy/skynet/game/ &> /dev/null" && if [ $? '
                          '-eq 0 ];then echo "success";else echo "error";fi') as p:
                by_git_pull = p.read()
            with os.popen(
                    'ssh root@120.76.174.183 "cd /home/hlby/HuanLe_server && git rev-parse --short HEAD"') as p:
                git_byhash = p.read()
            with os.popen('ssh root@8.129.217.169 "cd /home/jy/skynet && ./kill.sh aliyun_test_single && '
                          'cd logs/ && rm -rf *.log *.pid" && if [ $? '
                          '-eq 0 ];then echo "success";else echo "error";fi') as p:
                by_stop = p.read()
            if 'success' in by_git_pull and 'success' in by_stop:
                mes = "@%s\n欢乐天天捕鱼预发布已停止，将立即启动" % data.post_user
                requests.post(url=webhook, json=messge(mes), headers=headers)
                with os.popen('ssh root@8.129.217.169 "cd /home/jy/skynet/ && ./skynet '
                              'game/launch/aliyun_test_single/single_config.lua" && if [ $? '
                              '-eq 0 ];then echo "success";else echo "error";fi') as p:
                    by_start = p.read()
                if 'success' in by_start:
                    mes = "@%s\n欢乐天天捕鱼预发布已启动完成\n当前分支版本为:%s" % (data.post_user, git_byhash)
                    requests.post(url=webhook, json=messge(mes), headers=headers)
                    return ''
                else:
                    mes = "@%s\n欢乐天天捕鱼预发布启动失败" % data.post_user
                    requests.post(url=webhook, json=messge(mes), headers=headers)
                    return ''
            else:
                mes = "@%s\n欢乐天天捕鱼预发布停止失败" % data.post_user
                requests.post(url=webhook, json=messge(mes), headers=headers)
                return ''
        elif data.post_mes == 'help' or data.post_mes == '帮助':
            mes = "@%s\n选择1或者2执行相关操作：\n1.一键部署鲸鱼斗地主预发布\n2.一键部署欢乐天天捕鱼预发布" % data.post_user
            requests.post(url=webhook, json=messge(mes), headers=headers)
            return ''
        elif data.post_user not in adminname:
            mes = "@%s\n你没有权限执行操作" % data.post_user
            requests.post(url=webhook, json=messge(mes), headers=headers)
            return ''
        else:
            mes = "@%s\n参数不对\n输入help或帮助获取相关信息。" % data.post_user
            requests.post(url=webhook, json=messge(mes), headers=headers)
            return ''
    else:
        return "请求不合法"


@app.route('/', methods=['GET'])
def get():
    return "别瞅"


if __name__ == '__main__':
    app.run('0.0.0.0', 8090, debug=True)
