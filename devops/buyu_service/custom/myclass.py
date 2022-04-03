from flask import request
import configparser
import os
import json
import base64
import shutil
import hashlib


# 文件相关类
class OpenFiles(object):
    config = configparser.ConfigParser()
    delitem = configparser.ConfigParser()
    install_info = configparser.ConfigParser()
    main_info = configparser.ConfigParser()

    # 打开配置文件
    def readconfig(self):
        self.config.read('config.ini', encoding='utf-8')
        return self.config

    # 打开删除项目信息文件
    def readelitem(self):
        self.delitem.read('status/删除项目信息.conf', encoding='utf-8')
        return self.delitem

    # 打开项目安装包信息文件
    def readinstall(self):
        self.install_info.read('status/项目安装包信息.ini', encoding='utf-8')
        return self.install_info

    # 打开维护设置信息文件
    def readmain(self):
        self.main_info.read('status/维护设置信息.ini', encoding='utf-8')
        return self.main_info


# 路径相关类
class Explorer(OpenFiles):
    def __init__(self, arg):
        super().__init__()
        self.update = self.readconfig()[arg]['update']
        self.update_exp = os.path.join(self.readconfig()[arg]['update'], arg)
        self.adr_exp = os.path.join(self.update_exp, 'Android')
        self.ios_exp = os.path.join(self.update_exp, 'IOS')
        self.conf_exp = os.path.join(self.update_exp, 'localconfig')
        self.res_exp = os.path.join(self.update_exp, 'Resource')
        self.adr_vermap = os.path.join(self.adr_exp, 'version_map.txt')
        self.ios_vermap = os.path.join(self.ios_exp, 'version_map.txt')
        self.recycle = os.path.join('C:\\Program Files\\servers\\buyu_service\\recycle', arg)


# 项目相关类
class NewItem_POST(object):
    # 初始化类属性
    def __init__(self, args):
        self.username = args.get('username').strip()
        self.itemname = args.get('itemname').strip()
        self.install = args.get('install').strip()
        self.test = args.get('test').strip()
        self.update = args.get('update').strip()


# 删除项目相关类
class DelItem_POST(object):
    def __init__(self, args):
        self.username = args.get('username').strip()
        self.itemname = args.get('itemname')
        self.recovery = str(args.get('recovery')).strip()


# 发布安装包POST类
class Install_POST(object):
    def __init__(self, args):
        self.info = args


# 发布超热更相关类
class Hot_Get(Explorer, OpenFiles):
    def __init__(self):
        self.default = []
        self.version = {}

    def hotget(self):
        for i in self.readconfig().sections():
            super().__init__(i)
            if self.readconfig()[i]['itemname']:
                itemname = {'itemname': i}
                versionlist = {"versionlist": os.listdir(self.conf_exp)}
                for k in os.listdir(self.update_exp):
                    if k == 'Android':
                        with open(self.adr_vermap, 'r', encoding='utf-8') as adr:
                            get_version = json.load(adr)
                        self.version = {'android': {'version': get_version['last_version'], 'last_version': get_version['config_version']}}
                        itemname.update(self.version)
                    elif k == 'IOS':
                        with open(self.ios_vermap, 'r', encoding='utf-8') as apple:
                            get_version = json.load(apple)
                        self.version = {'ios': {'version': get_version['last_version'], 'last_version': get_version['config_version']}}
                        itemname.update(self.version)
                    elif k != 'IOS' and k != 'Android':
                        continue
                    else:
                        return {'news': 'error', 'info': '请求失败'}
                itemname.update(versionlist)
                self.default.append(itemname)
        return {'data': self.default}


class Hot_Post(Explorer):
    def __init__(self, args):
        for i in args:
            super().__init__(i)
            self.adr_version_exp = os.path.join(self.conf_exp, args[i]['android']['set_version'])
            self.adr_set_version = args[i]['android']['set_version']
            self.adr_merg = args[i]['android']['merg']
            self.adr_files = args[i]['android']['files']
            self.adr_last_version = os.path.join(self.conf_exp, args[i]['android']['last_version'])
            self.adr_md5_file = os.path.join(self.adr_version_exp, 'file_list.txt')
            self.ios_version_exp = os.path.join(self.conf_exp, args[i]['ios']['set_version'])
            self.ios_set_version = args[i]['ios']['set_version']
            self.ios_merg = args[i]['ios']['merg']
            self.ios_files = args[i]['ios']['files']
            self.ios_last_version = os.path.join(self.conf_exp, args[i]['ios']['last_version'])
            self.ios_md5_file = os.path.join(self.ios_version_exp, 'file_list.txt')

    def mk_version_dir(self):
        try:
            if self.adr_set_version and self.ios_set_version and self.adr_set_version == self.ios_set_version:
                if self.adr_merg == 'true' and self.ios_merg == 'true':
                    shutil.copytree(self.adr_last_version, self.adr_version_exp)
                    for i in self.adr_files:
                        if i['name'].split('.')[1] == 'lua' or i['name'].split('.')[1] == 'txt':
                            with open(os.path.join(self.adr_version_exp, i['name']), 'w', encoding='utf-8') as adr_text:
                                adr_text.write(i['value'])
                        else:
                            with open(os.path.join(self.res_exp, i['name']), 'wb') as adr_bytes:
                                adr_bytes.write(base64.b64decode(i['value'].split(',')[1]))
                    return {'news': 'succesee', 'info': '热更文件保存成功'}
                elif self.adr_merg == 'false' and self.ios_merg == 'false':
                    os.mkdir(self.adr_version_exp)
                    for i in self.adr_files:
                        if i['name'].split('.')[1] == 'lua' or i['name'].split('.')[1] == 'txt':
                            with open(os.path.join(self.adr_version_exp, i['name']), 'w', encoding='utf-8') as adr_text:
                                adr_text.write(i['value'])
                        else:
                            with open(os.path.join(self.res_exp, i['name']), 'wb') as adr_bytes:
                                adr_bytes.write(base64.b64decode(i['value'].split(',')[1]))
                    return {'news': 'succesee', 'info': '热更文件保存成功'}
                else:
                    return {'news': 'error', 'info': '不支持此组合参数操作'}
            elif self.adr_set_version and self.ios_set_version and self.adr_set_version != self.ios_set_version:
                if self.adr_merg == 'true' and self.ios_merg == 'true':
                    shutil.copytree(self.adr_last_version, self.adr_version_exp)
                    shutil.copytree(self.ios_last_version, self.ios_version_exp)
                    for i in self.adr_files:
                        if i['name'].split('.')[1] == 'lua' or i['name'].split('.')[1] == 'txt':
                            with open(os.path.join(self.adr_version_exp, i['name']), 'w', encoding='utf-8') as adr_text:
                                adr_text.write(i['value'])
                        else:
                            with open(os.path.join(self.res_exp, i['name']), 'wb') as adr_bytes:
                                adr_bytes.write(base64.b64decode(i['value'].split(',')[1]))
                    for f in self.ios_files:
                        if f['name'].split('.')[1] == 'lua' or f['name'].split('.')[1] == 'txt':
                            with open(os.path.join(self.ios_version_exp, f['name']), 'w', encoding='utf-8') as ios_text:
                                ios_text.write(f['value'])
                        else:
                            with open(os.path.join(self.res_exp, f['name']), 'wb') as ios_bytes:
                                ios_bytes.write(base64.b64decode(f['value'].split(',')[1]))
                    return {'news': 'succesee', 'info': '热更文件保存成功'}
                elif self.adr_merg == 'true' and self.ios_merg == 'false':
                    shutil.copytree(self.adr_last_version, self.adr_version_exp)
                    os.mkdir(self.ios_version_exp)
                    for i in self.adr_files:
                        if i['name'].split('.')[1] == 'lua' or i['name'].split('.')[1] == 'txt':
                            with open(os.path.join(self.adr_version_exp, i['name']), 'w', encoding='utf-8') as adr_text:
                                adr_text.write(i['value'])
                        else:
                            with open(os.path.join(self.res_exp, i['name']), 'wb') as adr_text:
                                adr_text.write(base64.b64decode(i['value'].split(',')[1]))
                    for f in self.ios_files:
                        if f['name'].split('.')[1] == 'lua' or f['name'].split('.')[1] == 'txt':
                            with open(os.path.join(self.ios_version_exp, f['name']), 'w', encoding='utf-8') as ios_text:
                                ios_text.write(f['value'])
                        else:
                            with open(os.path.join(self.res_exp, f['name']), 'wb') as ios_bytes:
                                ios_bytes.write(base64.b64decode(f['value'].split(',')[1]))
                    return {'news': 'succesee', 'info': '热更文件保存成功'}
                elif self.adr_merg == 'false' and self.ios_merg == 'true':
                    os.mkdir(self.adr_version_exp)
                    shutil.copytree(self.ios_last_version, self.ios_version_exp)
                    for i in self.adr_files:
                        if i['name'].split('.')[1] == 'lua' or i['name'].split('.')[1] == 'txt':
                            with open(os.path.join(self.adr_version_exp, i['name']), 'w', encoding='utf-8') as adr_text:
                                adr_text.write(i['value'])
                        else:
                            with open(os.path.join(self.res_exp, i['name']), 'wb') as adr_text:
                                adr_text.write(base64.b64decode(i['value'].split(',')[1]))
                    for f in self.ios_files:
                        if f['name'].split('.')[1] == 'lua' or f['name'].split('.')[1] == 'txt':
                            with open(os.path.join(self.ios_version_exp, f['name']), 'w', encoding='utf-8') as ios_text:
                                ios_text.write(f['value'])
                        else:
                            with open(os.path.join(self.res_exp, f['name']), 'wb') as ios_bytes:
                                ios_bytes.write(base64.b64decode(f['value'].split(',')[1]))
                    return {'news': 'succesee', 'info': '热更文件保存成功'}
                elif self.adr_merg == 'false' and self.ios_merg == 'false':
                    os.mkdir(self.adr_version_exp)
                    os.mkdir(self.ios_version_exp)
                    for i in self.adr_files:
                        if i['name'].split('.')[1] == 'lua' or i['name'].split('.')[1] == 'txt':
                            with open(os.path.join(self.adr_version_exp, i['name']), 'w', encoding='utf-8') as adr_text:
                                adr_text.write(i['value'])
                        else:
                            with open(os.path.join(self.res_exp, i['name']), 'wb') as adr_text:
                                adr_text.write(base64.b64decode(i['value'].split(',')[1]))
                    for f in self.ios_files:
                        if f['name'].split('.')[1] == 'lua' or f['name'].split('.')[1] == 'txt':
                            with open(os.path.join(self.ios_version_exp, f['name']), 'w', encoding='utf-8') as ios_text:
                                ios_text.write(f['value'])
                        else:
                            with open(os.path.join(self.res_exp, f['name']), 'wb') as ios_bytes:
                                ios_bytes.write(base64.b64decode(f['value'].split(',')[1]))
                    return {'news': 'succesee', 'info': '热更文件保存成功'}
                else:
                    return {'news': 'error', 'info': '不支持此组合参数操作'}
            elif self.adr_set_version and not self.ios_set_version:
                if self.adr_merg == 'true':
                    shutil.copytree(self.adr_last_version, self.adr_version_exp)
                    for i in self.adr_files:
                        if i['name'].split('.')[1] == 'lua' or i['name'].split('.')[1] == 'txt':
                            with open(os.path.join(self.adr_version_exp, i['name']), 'w', encoding='utf-8') as adr_text:
                                adr_text.write(i['value'])
                        else:
                            with open(os.path.join(self.res_exp, i['name']), 'wb') as adr_text:
                                adr_text.write(base64.b64decode(i['value'].split(',')[1]))
                    return {'news': 'succesee', 'info': '热更文件保存成功'}
                elif self.adr_merg == 'false':
                    os.mkdir(self.adr_version_exp)
                    for i in self.adr_files:
                        if i['name'].split('.')[1] == 'lua' or i['name'].split('.')[1] == 'txt':
                            with open(os.path.join(self.adr_version_exp, i['name']), 'w', encoding='utf-8') as adr_text:
                                adr_text.write(i['value'])
                        else:
                            with open(os.path.join(self.res_exp, i['name']), 'wb') as adr_text:
                                adr_text.write(base64.b64decode(i['value'].split(',')[1]))
                    return {'news': 'succesee', 'info': '热更文件保存成功'}
                else:
                    return {'news': 'error', 'info': '不支持此组合参数操作'}
            elif not self.adr_set_version and self.ios_set_version:
                if self.ios_merg == 'true':
                    shutil.copytree(self.ios_last_version, self.ios_version_exp)
                    for f in self.ios_files:
                        if f['name'].split('.')[1] == 'lua' or f['name'].split('.')[1] == 'txt':
                            with open(os.path.join(self.ios_version_exp, f['name']), 'w', encoding='utf-8') as ios_text:
                                ios_text.write(f['value'])
                        else:
                            with open(os.path.join(self.res_exp, f['name']), 'wb') as ios_bytes:
                                ios_bytes.write(base64.b64decode(f['value'].split(',')[1]))
                    return {'news': 'succesee', 'info': '热更文件保存成功'}
                elif self.adr_merg == 'false':
                    os.mkdir(self.ios_version_exp)
                    for f in self.ios_files:
                        if f['name'].split('.')[1] == 'lua' or f['name'].split('.')[1] == 'txt':
                            with open(os.path.join(self.ios_version_exp, f['name']), 'w', encoding='utf-8') as ios_text:
                                ios_text.write(f['value'])
                        else:
                            with open(os.path.join(self.res_exp, f['name']), 'wb') as ios_bytes:
                                ios_bytes.write(base64.b64decode(f['value'].split(',')[1]))
                    return {'news': 'succesee', 'info': '热更文件保存成功'}
                else:
                    return {'news': 'error', 'info': '不支持此组合参数操作'}
            else:
                return {'news': 'error', 'info': '不支持此组合参数操作'}
        except Exception as e:
            return {'news': 'error', 'info': '错误：%s' % e}


# 维护设置
class SetMain_GET(Explorer, OpenFiles):
    def __init__(self):
        self.default = []
        self.version = {}

    def mainget(self):
        for i in self.readconfig().sections():
            super().__init__(i)
            if self.readconfig()[i]['itemname']:
                itemname = {'itemname': i}
                for k in os.listdir(self.update_exp):
                    if k == 'Android':
                        self.version = {'android': {'version': os.listdir(self.adr_exp), 'localconfig': os.listdir(self.conf_exp)}}
                        itemname.update(self.version)
                    elif k == 'IOS':
                        self.version = {'ios': {'version': os.listdir(self.ios_exp), 'localconfig': os.listdir(self.conf_exp)}}
                        itemname.update(self.version)
                    elif k != 'IOS' and k != 'Android':
                        continue
                    else:
                        return {'news': 'error', 'info': '请求失败'}
                self.default.append(itemname)
        return {'data': self.default}


class SetMain_POST(Explorer):
    def __init__(self, args):
        for i in args:
            super().__init__(i)
            self.adr_version_exp = os.path.join(self.adr_exp, args[i]['android']['version'])
            self.adr_vermap = os.path.join(self.adr_version_exp, 'version_map.txt')
            self.adr_localconfig = os.path.join(self.conf_exp, args[i]['android']['localconfig'])
            self.adr_configfile = os.path.join(self.adr_localconfig, 'file_list.txt')
            self.ios_version_exp = os.path.join(self.ios_exp, args[i]['ios']['version'])
            self.ios_vermap = os.path.join(self.ios_version_exp, 'version_map.txt')
            self.ios_localconfig = os.path.join(self.conf_exp, args[i]['ios']['localconfig'])
            self.ios_configfile = os.path.join(self.ios_localconfig, 'file_list.txt')

    # 获取对应平台的MD5码
    def adr_md5(self):
        with open(self.adr_configfile, 'rb') as adr:
            adrmd5 = hashlib.md5(adr.read()).hexdigest()
        return adrmd5

    def ios_md5(self):
        with open(self.ios_configfile, 'rb') as ios:
            iosmd5 = hashlib.md5(ios.read()).hexdigest()
        return iosmd5


if __name__ == '__main__':
    from flask import request
    import configparser
    import os
    import json
    import base64
    import shutil
    import hashlib
