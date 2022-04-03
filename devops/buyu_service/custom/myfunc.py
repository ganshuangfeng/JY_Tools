from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from custom import myclass
from flask import request
import configparser
import hashlib
import shutil
import json
import time
import os


# 获取post数据
def post():
    post_data = json.loads(request.get_data().decode('utf-8'))
    return post_data


# 获取默认配置信息
def defconfig():
    config_options = myclass.OpenFiles().readconfig().items('default')
    config_options = dict(config_options)
    return config_options


# 获取项目和配置信息
def getconfig():
    config = myclass.OpenFiles().readconfig()
    s = []
    for i in config.sections():
        if config[i]['itemname']:
            s.append(dict(config.items(i)))
    return {'listitem': s}


# 新增项目写入配置文件并创建文件夹
def newitem():
    data = myclass.NewItem_POST(post())
    set_section = data.itemname
    config = myclass.OpenFiles().readconfig()
    try:
        config.add_section(set_section)
        for i in data.__dict__:
            config.set(set_section, i, str(data.__dict__[i]))
        with open('config.ini', 'w') as f:
            config.write(f)
        explorer = os.path.join(data.update, data.itemname)
        os.mkdir(explorer)
        os.mkdir(os.path.join(explorer, 'Android'))
        os.mkdir(os.path.join(explorer, 'IOS'))
        os.mkdir(os.path.join(explorer, 'localconfig'))
        os.mkdir(os.path.join(explorer, 'Resource'))
        return {'news': 'success', 'info': '保存成功'}
    except configparser.DuplicateSectionError:
        return {'news': 'error', 'info': '项目已存在:%s' % data.itemname}
    except FileNotFoundError:
        config.remove_section(set_section)
        with open('config.ini', 'w') as f:
            config.write(f)
        return {'news': 'error', 'info': '找不到指定路径:%s' % data.update}
    except FileExistsError:
        config.remove_section(set_section)
        with open('config.ini', 'w') as f:
            config.write(f)
        return {'news': 'error', 'info': '%s文件夹已存在' % data.itemname}


# 删除项目并移除文件夹
def delexplorer():
    data = myclass.DelItem_POST(post())
    delitem = myclass.OpenFiles().readelitem()
    try:
        config = myclass.Explorer(data.itemname)
        if delitem.has_section(data.itemname):
            return {'news': 'error', 'info': '删除失败，删除项目信息中有此项目'}
        else:
            shutil.move(config.update_exp, 'C:\\Program Files\\servers\\buyu_service\\recycle')
            delitem.add_section(data.itemname)
            for i in config.readconfig().options(data.itemname):
                delitem.set(data.itemname, i, config.readconfig()[data.itemname][i])
            delitem.set(data.itemname, 'username', data.username)
            delitem.set(data.itemname, 'recycle', config.recycle)
            with open('status/删除项目信息.conf', 'w') as d:
                delitem.write(d)
            with open('config.ini', 'w') as f:
                config.readconfig().remove_section(data.itemname)
                config.readconfig().write(f)
            return {'news': 'success', 'info': '成功删除'}
    except PermissionError:
        return {'news': 'error', 'info': '权限不足'}
    except shutil.Error:
        return {'news': 'error', 'info': '删除失败，回收站中有此项目'}
    except FileNotFoundError:
        with open('status/删除项目信息.conf', 'w') as b:
            delitem.remove_section(data.itemname)
            delitem.write(b)
        return {'news': 'error', 'info': '路径不存在此项目：%s' % config.update_exp}


# 恢复已删除项目
def recoveryitem():
    delitem = myclass.OpenFiles().readelitem()
    config = myclass.OpenFiles().readconfig()
    data = myclass.DelItem_POST(post())
    get_section = data.itemname
    try:
        for k in get_section:
            config.add_section(k)
            for i in delitem.options(k):
                config.set(k, i, delitem[k][i])
            with open('config.ini', 'w') as f:
                config.remove_option(k, 'recycle')
                config.write(f)
            shutil.move(delitem[k]['recycle'], delitem[k]['update'])
            with open('status/删除项目信息.conf', 'w') as d:
                delitem.remove_section(k)
                delitem.write(d)
        return {'news': 'success', 'info': '恢复成功'}
    except configparser.DuplicateSectionError:
        return {'news': 'error', 'info': '不可恢复！项目已存在:%s' % data.itemname}
    except PermissionError:
        config.remove_section(get_section)
        with open('config.ini', 'w') as f:
            config.write(f)
        return {'news': 'error', 'info': '权限不足'}


# 修改项目配置
def setitem():
    data = myclass.NewItem_POST(post())
    config = myclass.OpenFiles().readconfig()
    get_section = data.itemname
    try:
        for i in data.__dict__:
            config.set(get_section, i, str(data.__dict__[i]))
        with open('config.ini', 'w') as f:
            config.write(f)
        return {'news': 'success', 'info': '修改成功'}
    except Exception as e:
        return {'news': 'error', 'info': '修改失败，错误信息：%s' % e}


# 发布安装包
def releaseapk():
    data = myclass.Install_POST(post())
    config = myclass.OpenFiles().readconfig()
    install_info = myclass.OpenFiles().readinstall()
    try:
        for k in data.info:
            for i in install_info[k]['apkname'].split(','):
                explorer = os.path.join(config[k]['test'], i)
                shutil.copy(explorer, config[k]['install'])
        return {'news': 'success', 'info': '安装包发布成功'}
    except Exception as e:
        return {'news': 'error', 'info': '修改失败，错误信息：%s' % e}


# 发布超热更GET请求
def hotget():
    hot_get = myclass.Hot_Get()
    return hot_get.hotget()


# 发布超热更POST请求
def hotpost():
    username = post().get('username')
    release = post()['release']
    try:
        for i in post():
            if i != 'username' and i != 'release':
                item_info = {i: post().get(i)}
                hot_post = myclass.Hot_Post(dict(item_info))
                hot_post.mk_version_dir()
                if release == 'false' and hot_post.adr_set_version == hot_post.ios_set_version and hot_post.adr_set_version and hot_post.ios_set_version:
                    with open(hot_post.adr_md5_file, 'a') as md:
                        md.seek(0)
                        md.truncate()
                        for hot_files in os.listdir(hot_post.adr_version_exp):
                            if hot_files != 'file_list.txt':
                                with open(os.path.join(hot_post.adr_version_exp, hot_files), 'rb') as hot_file:
                                    md.write(hot_files + '|' + hashlib.md5(hot_file.read()).hexdigest() + '|#|' + str(
                                        os.path.getsize(os.path.join(hot_post.adr_version_exp, hot_files))) + '\n')
                    return {'news': 'success', 'info': 'MD5生成成功'}
                elif release == 'false' and hot_post.adr_version_exp != hot_post.ios_version_exp and hot_post.adr_set_version and hot_post.ios_set_version:
                    with open(hot_post.adr_md5_file, 'a') as md:
                        md.seek(0)
                        md.truncate()
                        for hot_files in os.listdir(hot_post.adr_version_exp):
                            if hot_files != 'file_list.txt':
                                with open(os.path.join(hot_post.adr_version_exp, hot_files), 'rb') as hot_file:
                                    md.write(hot_files + '|' + hashlib.md5(hot_file.read()).hexdigest() + '|#|' + str(
                                        os.path.getsize(os.path.join(hot_post.adr_version_exp, hot_files))) + '\n')
                    with open(hot_post.ios_md5_file, 'a') as ios_md:
                        ios_md.seek(0)
                        ios_md.truncate()
                        for hot_files in os.listdir(hot_post.ios_version_exp):
                            if hot_files != 'file_list.txt':
                                with open(os.path.join(hot_post.ios_version_exp, hot_files), 'rb') as hot_file:
                                    ios_md.write(
                                        hot_files + '|' + hashlib.md5(hot_file.read()).hexdigest() + '|#|' + str(
                                            os.path.getsize(os.path.join(hot_post.ios_version_exp, hot_files))) + '\n')
                    return {'news': 'success', 'info': 'MD5生成成功'}
                elif release == 'false' and hot_post.adr_set_version and not hot_post.ios_set_version:
                    with open(hot_post.adr_md5_file, 'a') as md:
                        md.seek(0)
                        md.truncate()
                        for hot_files in os.listdir(hot_post.adr_version_exp):
                            if hot_files != 'file_list.txt':
                                with open(os.path.join(hot_post.adr_version_exp, hot_files), 'rb') as hot_file:
                                    md.write(hot_files + '|' + hashlib.md5(hot_file.read()).hexdigest() + '|#|' + str(
                                        os.path.getsize(os.path.join(hot_post.adr_version_exp, hot_files))) + '\n')
                    return {'news': 'success', 'info': 'MD5生成成功'}
                elif release == 'false' and not hot_post.adr_set_version and hot_post.ios_set_version:
                    with open(hot_post.ios_md5_file, 'a') as ios_md:
                        ios_md.seek(0)
                        ios_md.truncate()
                        for hot_files in os.listdir(hot_post.ios_version_exp):
                            if hot_files != 'file_list.txt':
                                with open(os.path.join(hot_post.ios_version_exp, hot_files), 'rb') as hot_file:
                                    ios_md.write(
                                        hot_files + '|' + hashlib.md5(hot_file.read()).hexdigest() + '|#|' + str(
                                            os.path.getsize(os.path.join(hot_post.ios_version_exp, hot_files))) + '\n')
                    return {'news': 'success', 'info': 'MD5生成成功'}
                elif release == 'true' and hot_post.adr_set_version == hot_post.ios_set_version and hot_post.adr_set_version and hot_post.ios_set_version:
                    with open(hot_post.adr_md5_file, 'w') as md:
                        md.seek(0)
                        md.truncate()
                        for hot_files in os.listdir(hot_post.adr_version_exp):
                            if hot_files != 'file_list.txt':
                                with open(os.path.join(hot_post.adr_version_exp, hot_files), 'rb') as hot_file:
                                    md.write(hot_files + '|' + hashlib.md5(hot_file.read()).hexdigest() + '|#|' + str(
                                        os.path.getsize(os.path.join(hot_post.adr_version_exp, hot_files))) + '\n')
                    with open(hot_post.adr_md5_file, 'rb') as md5_config:
                        config_md5 = hashlib.md5(md5_config.read()).hexdigest()
                    with open(hot_post.adr_vermap, 'r+') as adr_ver:
                        adr_ver_read = json.load(adr_ver)
                        adr_ver.seek(0)
                        adr_ver.truncate()
                        adr_ver_read['config_version'] = post()[i]['android']['set_version']
                        adr_ver_read['config_md5'] = config_md5
                        json.dump(adr_ver_read, adr_ver)
                    with open(hot_post.ios_vermap, 'r+') as ios_ver:
                        ios_ver_read = json.load(ios_ver)
                        ios_ver.seek(0)
                        ios_ver.truncate()
                        ios_ver_read['config_version'] = post()[i]['ios']['set_version']
                        ios_ver_read['config_md5'] = config_md5
                        json.dump(ios_ver_read, ios_ver)
                    return {'news': 'success', 'info': '发布成功'}
                elif release == 'true' and hot_post.adr_set_version != hot_post.ios_set_version and hot_post.adr_set_version and hot_post.ios_set_version:
                    with open(hot_post.adr_md5_file, 'w') as md:
                        md.seek(0)
                        md.truncate()
                        for hot_files in os.listdir(hot_post.adr_version_exp):
                            if hot_files != 'file_list.txt':
                                with open(os.path.join(hot_post.adr_version_exp, hot_files), 'rb') as hot_file:
                                    md.write(hot_files + '|' + hashlib.md5(hot_file.read()).hexdigest() + '|#|' + str(
                                        os.path.getsize(os.path.join(hot_post.adr_version_exp, hot_files))) + '\n')
                    with open(hot_post.ios_md5_file, 'w') as ios_md:
                        ios_md.seek(0)
                        ios_md.truncate()
                        for hot_files in os.listdir(hot_post.ios_version_exp):
                            if hot_files != 'file_list.txt':
                                with open(os.path.join(hot_post.ios_version_exp, hot_files), 'rb') as hot_file:
                                    ios_md.write(
                                        hot_files + '|' + hashlib.md5(hot_file.read()).hexdigest() + '|#|' + str(
                                            os.path.getsize(os.path.join(hot_post.ios_version_exp, hot_files))) + '\n')
                    with open(hot_post.adr_md5_file, 'rb') as adr_md5_config:
                        adr_config_md5 = hashlib.md5(adr_md5_config.read()).hexdigest()
                    with open(hot_post.ios_md5_file, 'rb') as ios_md5_config:
                        ios_config_md5 = hashlib.md5(ios_md5_config.read()).hexdigest()
                    with open(hot_post.adr_vermap, 'r+') as adr_ver:
                        adr_ver_read = json.load(adr_ver)
                        adr_ver.seek(0)
                        adr_ver.truncate()
                        adr_ver_read['config_version'] = post()[i]['android']['set_version']
                        adr_ver_read['config_md5'] = adr_config_md5
                        json.dump(adr_ver_read, adr_ver)
                    with open(hot_post.ios_vermap, 'r+') as ios_ver:
                        ios_ver_read = json.load(ios_ver)
                        ios_ver.seek(0)
                        ios_ver.truncate()
                        ios_ver_read['config_version'] = post()[i]['ios']['set_version']
                        ios_ver_read['config_md5'] = ios_config_md5
                        json.dump(ios_ver_read, ios_ver)
                    return {'news': 'success', 'info': '发布成功'}
                elif release == 'true' and hot_post.adr_set_version and not hot_post.ios_set_version:
                    with open(hot_post.adr_md5_file, 'w') as md:
                        md.seek(0)
                        md.truncate()
                        for hot_files in os.listdir(hot_post.adr_version_exp):
                            if hot_files != 'file_list.txt':
                                with open(os.path.join(hot_post.adr_version_exp, hot_files), 'rb') as hot_file:
                                    md.write(hot_files + '|' + hashlib.md5(hot_file.read()).hexdigest() + '|#|' + str(
                                        os.path.getsize(os.path.join(hot_post.adr_version_exp, hot_files))) + '\n')
                    with open(hot_post.adr_md5_file, 'rb') as md5_config:
                        config_md5 = hashlib.md5(md5_config.read()).hexdigest()
                    with open(hot_post.adr_vermap, 'r+') as adr_ver:
                        adr_ver_read = json.load(adr_ver)
                        adr_ver.seek(0)
                        adr_ver.truncate()
                        adr_ver_read['config_version'] = post()[i]['android']['set_version']
                        adr_ver_read['config_md5'] = config_md5
                        json.dump(adr_ver_read, adr_ver)
                    return {'news': 'success', 'info': '发布成功'}
                elif release == 'true' and not hot_post.adr_set_version and hot_post.ios_set_version:
                    with open(hot_post.ios_md5_file, 'a') as ios_md:
                        ios_md.seek(0)
                        ios_md.truncate()
                        for hot_files in os.listdir(hot_post.ios_version_exp):
                            if hot_files != 'file_list.txt':
                                with open(os.path.join(hot_post.ios_version_exp, hot_files), 'rb') as hot_file:
                                    ios_md.write(
                                        hot_files + '|' + hashlib.md5(hot_file.read()).hexdigest() + '|#|' + str(
                                            os.path.getsize(os.path.join(hot_post.ios_version_exp, hot_files))) + '\n')
                    with open(hot_post.ios_md5_file, 'rb') as md5_config:
                        config_md5 = hashlib.md5(md5_config.read()).hexdigest()
                    with open(hot_post.ios_vermap, 'r+') as ios_ver:
                        ios_ver_read = json.load(ios_ver)
                        ios_ver.seek(0)
                        ios_ver.truncate()
                        ios_ver_read['config_version'] = post()[i]['ios']['set_version']
                        ios_ver_read['config_md5'] = config_md5
                        json.dump(ios_ver_read, ios_ver)
                    return {'news': 'success', 'info': '发布成功'}
                else:
                    return {'news': 'error', 'info': '操作失败'}
    except FileNotFoundError as err:
        return {'news': 'error', 'info': '文件不存在！%s' % err}


# 维护设置
def set_main_get():
    main_get = myclass.SetMain_GET()
    return main_get.mainget()


def set_main_post():
    main_conf = configparser.ConfigParser()
    main_conf.read('status/维护设置信息.ini', encoding='utf-8')
    username = post()['username']
    execution = post()['execution']
    server_status = post()['server_status']
    restart = post()['restart']
    if post()['time'] and int(post()['time']) / 1000 <= time.time():
        return {'news': 'error', 'info': '预约时间不能小于当前时间'}
    elif main_conf.has_section('default'):
        return {'news': 'error', 'info': '只能预约一次，请在执行后预约。'}
    set_time = post()['time']
    try:
        if execution == 'false' and server_status and set_time and not main_conf.has_section('default'):
            main_conf.add_section('default')
            main_conf.set('default', 'username', username)
            main_conf.set('default', 'server_status', server_status)
            main_conf.set('default', 'time', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(set_time) / 1000)))
            main_conf.set('default', 'execution', execution)
            main_conf.set('default', 'restart', restart)
            for i in post():
                if i != 'server_status' and i != 'time' and i != 'execution' and i != 'restart' and i != 'username':
                    item_info = {i: post().get(i)}
                    data = myclass.SetMain_POST(dict(item_info))
                    if post()[i]['android']['version'] and post()[i]['ios']['version'] and post()[i]['android'][
                        'localconfig'] and post()[i]['ios']['localconfig']:
                        main_conf.add_section(i)
                        main_conf.set(i, 'adr_local', post()[i]['android']['localconfig'])
                        main_conf.set(i, 'adr_version', post()[i]['android']['version'])
                        main_conf.set(i, 'adr_md5', data.adr_md5())
                        main_conf.set(i, 'adr_version_map', data.adr_vermap)
                        main_conf.set(i, 'adr_exp', os.path.join(data.adr_exp, 'version_map.txt'))
                        main_conf.set(i, 'ios_local', post()[i]['ios']['localconfig'])
                        main_conf.set(i, 'ios_version', post()[i]['ios']['version'])
                        main_conf.set(i, 'ios_md5', data.ios_md5())
                        main_conf.set(i, 'ios_version_map', data.ios_vermap)
                        main_conf.set(i, 'ios_exp', os.path.join(data.ios_exp, 'version_map.txt'))
                        with open('status/维护设置信息.ini', 'w', encoding='utf-8') as f:
                            main_conf.write(f)
                        with open(data.adr_vermap, 'r+', encoding='utf-8') as adr_r:
                            adr_ver = json.load(adr_r)
                            adr_r.seek(0)
                            adr_r.truncate()
                            adr_ver['config_version'] = main_conf[i]['adr_local']
                            adr_ver['config_md5'] = main_conf[i]['adr_md5']
                            adr_ver['server_status'] = main_conf['default']['server_status']
                            if main_conf['default']['restart'] == 'true':
                                adr_ver['restart'] = 'true'
                                json.dump(adr_ver, adr_r, ensure_ascii=False)
                            else:
                                json.dump(adr_ver, adr_r, ensure_ascii=False)
                        with open(data.ios_vermap, 'r+', encoding='utf-8') as ios_r:
                            ios_ver = json.load(ios_r)
                            ios_r.seek(0)
                            ios_r.truncate()
                            ios_ver['config_version'] = main_conf[i]['ios_local']
                            ios_ver['config_md5'] = main_conf[i]['ios_md5']
                            ios_ver['server_status'] = main_conf['default']['server_status']
                            if main_conf['default']['restart'] == 'true':
                                adr_ver['restart'] = 'true'
                                json.dump(ios_ver, ios_r, ensure_ascii=False)
                            else:
                                json.dump(ios_ver, ios_r, ensure_ascii=False)
                    elif post()[i]['android']['version'] and post()[i]['ios']['version'] and post()[i]['android'][
                        'localconfig'] and not post()[i]['ios']['localconfig']:
                        main_conf.add_section(i)
                        main_conf.set(i, 'adr_local', post()[i]['android']['localconfig'])
                        main_conf.set(i, 'adr_version', post()[i]['android']['version'])
                        main_conf.set(i, 'adr_md5', data.adr_md5())
                        main_conf.set(i, 'adr_version_map', data.adr_vermap)
                        main_conf.set(i, 'adr_exp', os.path.join(data.adr_exp, 'version_map.txt'))
                        main_conf.set(i, 'ios_version', post()[i]['ios']['version'])
                        main_conf.set(i, 'ios_version_map', data.ios_vermap)
                        main_conf.set(i, 'ios_exp', os.path.join(data.ios_exp, 'version_map.txt'))
                        with open('status/维护设置信息.ini', 'w', encoding='utf-8') as f:
                            main_conf.write(f)
                        with open(data.adr_vermap, 'r+', encoding='utf-8') as adr_r:
                            adr_ver = json.load(adr_r)
                            adr_r.seek(0)
                            adr_r.truncate()
                            adr_ver['config_version'] = main_conf[i]['adr_local']
                            adr_ver['config_md5'] = main_conf[i]['adr_md5']
                            adr_ver['server_status'] = main_conf['default']['server_status']
                            if main_conf['default']['restart'] == 'true':
                                adr_ver['restart'] = 'true'
                                json.dump(adr_ver, adr_r, ensure_ascii=False)
                            else:
                                json.dump(adr_ver, adr_r, ensure_ascii=False)
                        with open(data.ios_vermap, 'r+', encoding='utf-8') as ios_r:
                            ios_ver = json.load(ios_r)
                            ios_r.seek(0)
                            ios_r.truncate()
                            ios_ver['config_version'] = ''
                            ios_ver['config_md5'] = ''
                            ios_ver['server_status'] = main_conf['default']['server_status']
                            if main_conf['default']['restart'] == 'true':
                                adr_ver['restart'] = 'true'
                                json.dump(ios_ver, ios_r, ensure_ascii=False)
                            else:
                                json.dump(ios_ver, ios_r, ensure_ascii=False)
                    elif post()[i]['android']['version'] and post()[i]['ios']['version'] and not post()[i]['android'][
                        'localconfig'] and post()[i]['ios']['localconfig']:
                        main_conf.add_section(i)
                        main_conf.set(i, 'adr_version', post()[i]['android']['version'])
                        main_conf.set(i, 'adr_version_map', data.adr_vermap)
                        main_conf.set(i, 'adr_exp', os.path.join(data.adr_exp, 'version_map.txt'))
                        main_conf.set(i, 'ios_local', post()[i]['ios']['localconfig'])
                        main_conf.set(i, 'ios_version', post()[i]['ios']['version'])
                        main_conf.set(i, 'ios_md5', data.ios_md5())
                        main_conf.set(i, 'ios_version_map', data.ios_vermap)
                        main_conf.set(i, 'ios_exp', os.path.join(data.ios_exp, 'version_map.txt'))
                        with open('status/维护设置信息.ini', 'w', encoding='utf-8') as f:
                            main_conf.write(f)
                        with open(data.adr_vermap, 'r+', encoding='utf-8') as adr_r:
                            adr_ver = json.load(adr_r)
                            adr_r.seek(0)
                            adr_r.truncate()
                            adr_ver['config_version'] = ''
                            adr_ver['config_md5'] = ''
                            adr_ver['server_status'] = main_conf['default']['server_status']
                            if main_conf['default']['restart'] == 'true':
                                adr_ver['restart'] = 'true'
                                json.dump(adr_ver, adr_r, ensure_ascii=False)
                            else:
                                json.dump(adr_ver, adr_r, ensure_ascii=False)
                        with open(data.ios_vermap, 'r+', encoding='utf-8') as ios_r:
                            ios_ver = json.load(ios_r)
                            ios_r.seek(0)
                            ios_r.truncate()
                            ios_ver['config_version'] = main_conf[i]['ios_local']
                            ios_ver['config_md5'] = main_conf[i]['ios_md5']
                            ios_ver['server_status'] = main_conf['default']['server_status']
                            if main_conf['default']['restart'] == 'true':
                                adr_ver['restart'] = 'true'
                                json.dump(ios_ver, ios_r, ensure_ascii=False)
                            else:
                                json.dump(ios_ver, ios_r, ensure_ascii=False)
                    elif post()[i]['android']['version'] and post()[i]['ios']['version'] and not post()[i]['android'][
                        'localconfig'] and not post()[i]['ios']['localconfig']:
                        main_conf.add_section(i)
                        main_conf.set(i, 'adr_version', post()[i]['android']['version'])
                        main_conf.set(i, 'adr_version_map', data.adr_vermap)
                        main_conf.set(i, 'adr_exp', os.path.join(data.adr_exp, 'version_map.txt'))
                        main_conf.set(i, 'ios_version', post()[i]['ios']['version'])
                        main_conf.set(i, 'ios_version_map', data.ios_vermap)
                        main_conf.set(i, 'ios_exp', os.path.join(data.ios_exp, 'version_map.txt'))
                        with open('status/维护设置信息.ini', 'w', encoding='utf-8') as f:
                            main_conf.write(f)
                        with open(data.adr_vermap, 'r+', encoding='utf-8') as adr_r:
                            adr_ver = json.load(adr_r)
                            adr_r.seek(0)
                            adr_r.truncate()
                            adr_ver['config_version'] = ''
                            adr_ver['config_md5'] = ''
                            adr_ver['server_status'] = main_conf['default']['server_status']
                            if main_conf['default']['restart'] == 'true':
                                adr_ver['restart'] = 'true'
                                json.dump(adr_ver, adr_r, ensure_ascii=False)
                            else:
                                json.dump(adr_ver, adr_r, ensure_ascii=False)
                        with open(data.ios_vermap, 'r+', encoding='utf-8') as ios_r:
                            ios_ver = json.load(ios_r)
                            ios_r.seek(0)
                            ios_r.truncate()
                            ios_ver['config_version'] = ''
                            ios_ver['config_md5'] = ''
                            ios_ver['server_status'] = main_conf['default']['server_status']
                            if main_conf['default']['restart'] == 'true':
                                adr_ver['restart'] = 'true'
                                json.dump(ios_ver, ios_r, ensure_ascii=False)
                            else:
                                json.dump(ios_ver, ios_r, ensure_ascii=False)
                    elif not post()[i]['android']['version'] and post()[i]['ios']['version'] and not \
                            post()[i]['android']['localconfig'] and post()[i]['ios']['localconfig']:
                        main_conf.add_section(i)
                        main_conf.set(i, 'ios_local', post()[i]['ios']['localconfig'])
                        main_conf.set(i, 'ios_version', post()[i]['ios']['version'])
                        main_conf.set(i, 'ios_md5', data.ios_md5())
                        main_conf.set(i, 'ios_version_map', data.ios_vermap)
                        main_conf.set(i, 'ios_exp', os.path.join(data.ios_exp, 'version_map.txt'))
                        with open('status/维护设置信息.ini', 'w', encoding='utf-8') as f:
                            main_conf.write(f)
                        with open(data.ios_vermap, 'r+', encoding='utf-8') as ios_r:
                            ios_ver = json.load(ios_r)
                            ios_r.seek(0)
                            ios_r.truncate()
                            ios_ver['config_version'] = main_conf[i]['ios_local']
                            ios_ver['config_md5'] = main_conf[i]['ios_md5']
                            ios_ver['server_status'] = main_conf['default']['server_status']
                            if main_conf['default']['restart'] == 'true':
                                adr_ver['restart'] = 'true'
                                json.dump(ios_ver, ios_r, ensure_ascii=False)
                            else:
                                json.dump(ios_ver, ios_r, ensure_ascii=False)
                    elif not post()[i]['android']['version'] and post()[i]['ios']['version'] and not \
                            post()[i]['android']['localconfig'] and not post()[i]['ios']['localconfig']:
                        main_conf.add_section(i)
                        main_conf.set(i, 'ios_version', post()[i]['ios']['version'])
                        main_conf.set(i, 'ios_version_map', data.ios_vermap)
                        main_conf.set(i, 'ios_exp', os.path.join(data.ios_exp, 'version_map.txt'))
                        with open('status/维护设置信息.ini', 'w', encoding='utf-8') as f:
                            main_conf.write(f)
                        with open(data.ios_vermap, 'r+', encoding='utf-8') as ios_r:
                            ios_ver = json.load(ios_r)
                            ios_r.seek(0)
                            ios_r.truncate()
                            ios_ver['config_version'] = ''
                            ios_ver['config_md5'] = ''
                            ios_ver['server_status'] = main_conf['default']['server_status']
                            if main_conf['default']['restart'] == 'true':
                                adr_ver['restart'] = 'true'
                                json.dump(ios_ver, ios_r, ensure_ascii=False)
                            else:
                                json.dump(ios_ver, ios_r, ensure_ascii=False)
                    elif post()[i]['android']['version'] and not post()[i]['ios']['version'] and post()[i]['android'][
                        'localconfig'] and not post()[i]['ios']['localconfig']:
                        main_conf.add_section(i)
                        main_conf.set(i, 'adr_local', post()[i]['android']['localconfig'])
                        main_conf.set(i, 'adr_version', post()[i]['android']['version'])
                        main_conf.set(i, 'adr_md5', data.adr_md5())
                        main_conf.set(i, 'adr_version_map', data.adr_vermap)
                        main_conf.set(i, 'adr_exp', os.path.join(data.adr_exp, 'version_map.txt'))
                        with open('status/维护设置信息.ini', 'w', encoding='utf-8') as f:
                            main_conf.write(f)
                        with open(data.adr_vermap, 'r+', encoding='utf-8') as adr_r:
                            adr_ver = json.load(adr_r)
                            adr_r.seek(0)
                            adr_r.truncate()
                            adr_ver['config_version'] = main_conf[i]['adr_local']
                            adr_ver['config_md5'] = main_conf[i]['adr_md5']
                            adr_ver['server_status'] = main_conf['default']['server_status']
                            if main_conf['default']['restart'] == 'true':
                                adr_ver['restart'] = 'true'
                                json.dump(adr_ver, adr_r, ensure_ascii=False)
                            else:
                                json.dump(adr_ver, adr_r, ensure_ascii=False)
                    elif post()[i]['android']['version'] and not post()[i]['ios']['version'] and not \
                            post()[i]['android']['localconfig'] and not post()[i]['ios']['localconfig']:
                        main_conf.add_section(i)
                        main_conf.set(i, 'adr_version', post()[i]['android']['version'])
                        main_conf.set(i, 'adr_version_map', data.adr_vermap)
                        main_conf.set(i, 'adr_exp', os.path.join(data.adr_exp, 'version_map.txt'))
                        with open('status/维护设置信息.ini', 'w', encoding='utf-8') as f:
                            main_conf.write(f)
                        with open(data.adr_vermap, 'r+', encoding='utf-8') as adr_r:
                            adr_ver = json.load(adr_r)
                            adr_r.seek(0)
                            adr_r.truncate()
                            adr_ver['config_version'] = ''
                            adr_ver['config_md5'] = ''
                            adr_ver['server_status'] = main_conf['default']['server_status']
                            if main_conf['default']['restart'] == 'true':
                                adr_ver['restart'] = 'true'
                                json.dump(adr_ver, adr_r, ensure_ascii=False)
                            else:
                                json.dump(adr_ver, adr_r, ensure_ascii=False)
                    elif not post()[i]['android']['version'] and not post()[i]['ios']['version'] and not \
                            post()[i]['android']['localconfig'] and not post()[i]['ios']['localconfig']:
                        main_conf.remove_section(i)
                        main_conf.remove_section('default')
                        with open('status/维护设置信息.ini', 'w') as del_section:
                            main_conf.write(del_section)
                        return {'news': 'error', 'info': '格式不正确，请仔细检查！'}
                    else:
                        continue
            p = ThreadPoolExecutor(2)
            p.submit(time_run)
            return {'news': 'success', 'info': '预约成功'}
        elif execution == 'true' and server_status and not set_time:
            for i in post():
                if i != 'execution' and i != 'server_status' and i != 'username' and i != 'restart' and i != 'time':
                    get_config = myclass.Explorer(i)
                    for k in post()[i]:
                        if k == 'android' and 'Android' in os.listdir(get_config.update_exp) and 'version_map.txt' in os.listdir(get_config.adr_exp):
                            with open(get_config.adr_vermap, 'r+', encoding='utf-8') as adr_r:
                                adr_conf = json.load(adr_r)
                                adr_r.seek(0)
                                adr_r.truncate()
                                adr_conf['server_status'] = server_status
                                json.dump(adr_conf, adr_r, ensure_ascii=False)
                        elif k == 'ios' and 'IOS' in os.listdir(get_config.update_exp) and 'version_map.txt' in os.listdir(get_config.ios_exp):
                            with open(get_config.ios_vermap, 'r+', encoding='utf-8') as ios_r:
                                ios_conf = json.load(ios_r)
                                ios_r.seek(0)
                                ios_r.truncate()
                                ios_conf['server_status'] = server_status
                                json.dump(ios_conf, ios_r, ensure_ascii=False)
            return {'news': 'success', 'info': '执行成功'}
        elif execution == 'true' and set_time:
            return {'news': 'error', 'info': '请选择预约执行'}
        elif execution == 'true' and not server_status and not set_time:
            for i in post():
                if i != 'execution' and i != 'server_status' and i != 'username' and i != 'restart' and i != 'time':
                    get_config = myclass.Explorer(i)
                    for k in post()[i]:
                        if k == 'android' and 'Android' in os.listdir(get_config.update_exp) and 'version_map.txt' in os.listdir(get_config.adr_exp):
                            with open(get_config.adr_vermap, 'r+', encoding='utf-8') as adr_r:
                                adr_conf = json.load(adr_r)
                                adr_r.seek(0)
                                adr_r.truncate()
                                adr_conf['server_status'] = ''
                                json.dump(adr_conf, adr_r, ensure_ascii=False)
                        elif k == 'ios' and 'IOS' in os.listdir(get_config.update_exp) and 'version_map.txt' in os.listdir(get_config.ios_exp):
                            with open(get_config.ios_vermap, 'r+', encoding='utf-8') as ios_r:
                                ios_conf = json.load(ios_r)
                                ios_r.seek(0)
                                ios_r.truncate()
                                ios_conf['server_status'] = ''
                                json.dump(ios_conf, ios_r, ensure_ascii=False)
            return {'news': 'success', 'info': '执行成功'}
        else:
            return {'news': 'error', 'info': '格式不正确，请仔细核对。'}
    except FileNotFoundError as e:
        return {'news': 'error', 'info': '执行完成。有部分文件不存在！%s' % e}
    except configparser.DuplicateSectionError as e:
        return {'news': 'error', 'info': '只能预约一次，请在执行后预约！%s' % e}


def time_run():
    get_status = myclass.OpenFiles().readmain()
    while get_status.has_section('default'):
        if time.time() >= time.mktime(time.strptime(str(get_status['default']['time']), "%Y-%m-%d %H:%M:%S")):
            for k in get_status.sections():
                if k != 'default' and get_status.has_option(k, 'adr_version') and get_status.has_option(k, 'ios_version'):
                    shutil.copyfile(get_status[k]['adr_version_map'], get_status[k]['adr_exp'])
                    shutil.copyfile(get_status[k]['ios_version_map'], get_status[k]['ios_exp'])
                    get_status.remove_section(k)
                    get_status.remove_section('default')
                    with open('status/维护设置信息.ini', 'w') as del_section:
                        get_status.write(del_section)
                elif k != 'default' and get_status.has_option(k, 'adr_version') and not get_status.has_option(k, 'ios_version'):
                    shutil.copyfile(get_status[k]['adr_version_map'], get_status[k]['adr_exp'])
                    get_status.remove_section(k)
                    get_status.remove_section('default')
                    with open('status/维护设置信息.ini', 'w') as del_section:
                        get_status.write(del_section)
                elif k != 'default' and not get_status.has_option(k, 'adr_version') and get_status.has_option(k, 'ios_version'):
                    shutil.copyfile(get_status[k]['ios_version_map'], get_status[k]['adr_exp'])
                    get_status.remove_section(k)
                    get_status.remove_section('default')
                    with open('status/维护设置信息.ini', 'w') as del_section:
                        get_status.write(del_section)
        else:
            print('正在等待预约时间执行···')
            time.sleep(5)


# 预约状态信息
def main_stautus():
    main_info = myclass.OpenFiles().readmain()
    if len(main_info.sections()) <= 1:
        return {'news': 'success', 'info': '当前无预约！'}
    elif len(main_info.sections()) > 1:
        info = {'info': []}
        index = {'username': main_info['default']['username'], 'server_status': main_info['default']['server_status'],
                 'time': str(datetime.strptime(main_info['default']['time'], '%Y-%m-%d %H:%M:%S') - datetime.now()),
                 'restart': main_info['default']['restart']}
        for i in main_info.sections():
            if i != 'default':
                data = {'itemname': i, 'data': dict(main_info.items(i))}
                info['info'].append(data)
        index.update(info)
        return index


if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
    from datetime import datetime
    from custom import myclass
    from flask import request
    import configparser
    import hashlib
    import shutil
    import json
    import time
    import os
