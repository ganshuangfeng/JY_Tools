# Date:2021/1/11
# Author:peiyanfei
# 注：所有函数和变量名都用小写，类名使用驼峰。
# 通用配置，移动源码需要修改myclass和myfunc文件内共两处路径。
# 配置文件config.ini和项目安装包信息需要提前配置好。

from concurrent.futures import ThreadPoolExecutor
from custom import myclass, myfunc
from flask import Flask, request
import configparser
import base64
import json
import os
import shutil

app = Flask(__name__)


# 新增项目
@app.route('/newitem', methods=['GET', 'POST'])
def newitem():
    if request.method == 'GET':
        return json.dumps(myfunc.defconfig())
    elif request.method == 'POST':
        return json.dumps(myfunc.newitem())


# 删除项目
@app.route('/delitem', methods=['POST'])
def delitem():
    if request.method == 'GET':
        info = myclass.OpenFiles()
        return json.dumps({'itemname': list(info.readelitem().sections())})
    elif request.method == 'POST':
        data = myclass.DelItem_POST(myfunc.post())
        if data.recovery == 'true':
            return myfunc.recoveryitem()
        elif data.recovery == 'false':
            return myfunc.delexplorer()
        else:
            return {'news': 'error', 'info': '%s参数不合法' % data.recovery}


# 项目列表
@app.route('/listitem', methods=['GET'])
def listitem():
    return json.dumps(myfunc.getconfig())


# 配置项目
@app.route('/setitem', methods=['POST'])
def setitem():
    return myfunc.setitem()


# 发布安装包
@app.route('/install', methods=['POST'])
def install():
    return myfunc.releaseapk()


# 超热更
@app.route('/hotrelease', methods=['GET', 'POST'])
def hotrelease():
    if request.method == 'GET':
        return json.dumps(myfunc.hotget())
    elif request.method == 'POST':
        return json.dumps(myfunc.hotpost())


# 维护设置
@app.route('/setmain', methods=['GET', 'POST'])
def setmain():
    if request.method == 'GET':
        return json.dumps(myfunc.set_main_get())
    elif request.method == 'POST':
        return json.dumps(myfunc.set_main_post())


# 预约状态信息
@app.route('/mainstatus', methods=['GET'])
def mainstatus():
    return json.dumps(myfunc.main_stautus())


if __name__ == '__main__':
    app.run('0.0.0.0', 8090, debug=True)
