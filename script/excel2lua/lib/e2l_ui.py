#coding=utf-8
# ui - 用户界面

import os
import os.path
import xdrlib,sys
import xlrd
import types
import time
import e2l
import re
import shutil
import platform

reload(sys)
sys.setdefaultencoding( "utf-8" )

custom_version_folder = [
    "config_debug",
]

default_export_option = None

def set_default_export(_param):
    global default_export_option
    default_export_option = _param

def add_custom_version_folder(_folders):
    global custom_version_folder
    custom_version_folder.extend(_folders)

#获取脚本文件的当前路径
def cur_File_Dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

rootPath=cur_File_Dir()
# #获取上一级目录路径 根路径
rootPath=rootPath[:rootPath.rfind(os.sep)]
rootPath=rootPath[:rootPath.rfind(os.sep)]
tools_path = rootPath
rootPath=rootPath[:rootPath.rfind(os.sep)]

def eval_py_file(_file):
    file_object = open(_file,"r")
    if None == file_object:
        return None

    _ret = file_object.read()
    file_object.close()

    return eval(_ret)


# 参数 _item 用户中的选项
def export_default(_item,_cmd):

    e2l.export_all(
            os.path.join(_item["doc_dir"] , "config"),
            os.path.join(_item["doc_dir"] , "config", "export_config"))
    raw_input("input any key to continue ... ")

# 查找 配置拷贝列表： 
# 返回 None 或 文件列表 + 文件路径
def find_copy_file_list(_file_name,_dirs):

    for i,v in enumerate(_dirs):
        _tmp = os.path.join(v,"app_config",_file_name)
        if os.path.exists(_tmp):
            _list = eval_py_file(_tmp)
            for i in range(0,len(_list)):
                _list[i] = os.path.splitext(_list[i])[0]
            return _list,_tmp

    return None,None

    

# 得到 带日期后缀的 版本文件夹信息，例如： xxxxxxx_5.28 ， 返回 5,28
def get_version_folder_info(_name):
    m = re.search(r'_([0-9]{1,2})\.([0-9]{1,2})$',_name)
    if None == m:
        return 0,0
    if int(m.group(1)) == 0 or int(m.group(2)) == 0:
        return 0,0

    return int(m.group(1)),int(m.group(2))


# 检查输入的序号， 错误则继续，知道正确 或放弃
def input_select_index(_prompt,_max):
    while True:
        _sel = raw_input(_prompt)
        if "" == _sel:
            print u"放弃!"
            print
            return None
        m = re.search(r'^([0-9]+)$',_sel)
        if m == None:
            print u"错误的输入。请输入数字序号！"
            continue
        _sel_n = int(m.group(1))
        if _sel_n < 1 or _sel_n > _max:
            print u"输入序号超出范围！"
            continue
        return _sel_n

# 检查输入的序号（支持多个）， 错误则继续，知道正确 或放弃
def input_select_index_list(_prompt,_max):
    while True:
        _sel = raw_input(_prompt)
        if "" == _sel:
            print u"放弃!"
            print
            return None
        _list = _sel.split(",")
        _list_ret = []
        _err = False
        for v in _list:
            m = re.search(r'^([0-9]+)$',v)
            if m == None:
                print u"错误的输入。请输入数字序号！"
                _err = True
                break
            _sel_n = int(m.group(1))
            if _sel_n < 1 or _sel_n > _max:
                print u"输入序号超出范围！"
                _err = True
                break

            _list_ret.append(_sel_n)

        if _err:
            continue

        return _list_ret

def set2array(_set):
    ret = []
    for v in _set:
        ret.append(v)
    return ret

# 选择版本文件夹    
def select_version_folder(_item,_cmd_set):

    _doc_root = e2l.get_fullpath(rootPath,_item["doc_dir"])

    _set_custom_dir = set()
    _list_custom_dir = []  # 自定义 文件夹，排在最前面，并且 内部不参与排序

    for v in custom_version_folder:
        if v not in _set_custom_dir and os.path.exists(os.path.join(_doc_root,v)):
            _set_custom_dir.add(v)
            _list_custom_dir.append(v)
    
    _set_dirs = set()
    _set_dirs.add(".") # 当前文件夹也要加入
    for _filename in os.listdir(_doc_root):

        if os.path.isdir(os.path.join(_doc_root,_filename)):
            # 强制过滤掉 . 开始的
            if _filename in _set_custom_dir or  "." == _filename[:1]:
                continue
            if "a" in _cmd_set:
                _set_dirs.add(_filename)
            else:
                _month,_day = get_version_folder_info(_filename)
                if _month > 0 or _filename in _set_custom_dir:
                    _set_dirs.add(_filename)

    _array_dirs = set2array(_set_dirs)
    _array_dirs.sort()

    # 加入到 自定义的后面
    for v in _array_dirs:
        _list_custom_dir.append(v)

    if len(_list_custom_dir) < 1:
        print
        print u"没找到版本文件夹!"
        print
        raw_input("input any key to continue ... ")
        return None
        
    # 选择版本文件夹   
    print
    print u"+------------[版本文件夹列表]--------------+"
    for i,v in enumerate(_list_custom_dir):
        _month,_day = get_version_folder_info(v)
        if _month > 0:
            print u"|" + (" (%-2d月%-2d日)  " % (_month,_day)) + str(i+1) + ". " + v
        else:
            print u"|" + "             " + str(i+1)  + ". "  + v

    print u"+-----------------------------------------+"
    print

    if platform.system() == "Windows":
        _sel_n = input_select_index((u"请输入序号选择版本：").encode("GB2312"),len(_list_custom_dir))
    else:
        _sel_n = input_select_index(u"请输入序号选择版本：",len(_list_custom_dir))

    if None == _sel_n:
        return

    
    print u"已选择:",_list_custom_dir[_sel_n-1]
    return os.path.join(_doc_root,_list_custom_dir[_sel_n-1])

# 选择文件名，支持多个    
def select_files(_path):

    _list_files = []
    for _filename in os.listdir(_path):

        if not os.path.isdir(os.path.join(_path,_filename)):
            # 强制过滤掉 . 开始的
            if  "." == _filename[:1]:
                continue
            if  "~" == _filename[:1]:
                continue

            _list_files.append(_filename)
        
    # 选择版本文件夹   
    print
    print u"+------------[版本文件夹列表]--------------+"
    for i,v in enumerate(_list_files):
        print u"|" + " " + str(i+1)  + ". "  + v

    print u"+-----------------------------------------+"
    print

    if platform.system() == "Windows":
        _sel_n = input_select_index_list((u"请输入文件序号（多个用逗号分开）：").encode("GB2312"),len(_list_files))
    else:
        _sel_n = input_select_index_list("请输入文件序号（多个用逗号分开）：",len(_list_files))

    if None == _sel_n or len(_sel_n) == 0:
        return None

    ret_files = []
    for _sel in _sel_n:
        ret_files.append(_list_files[_sel-1])
    
    print u"已选择:",",".join(ret_files)

    return ret_files
        
# 选择输出文件夹    
def select_out_work_folder(_item):

    _doc_root = e2l.get_fullpath(rootPath,_item["doc_dir"])

    # 输出 root 的相对路径 以 _doc_root 为准
    _git_root = _doc_root[:_doc_root.rfind(os.sep)]

    if len(_item["ver_out"]) == 0:
            print u"项目没有配置输出文件夹(\"ver_out\")!"
            print
            return None
    
    # if len(_item["ver_out"]) == 1:  # 只有一个，则不需要选择
    #     print u"已默认使用:",_item["ver_out"][0]
    #     return e2l.get_fullpath(_git_root,_item["ver_out"][0])

    print
    print u"+------------[输出文件夹列表]--------------+"
    for i,v in enumerate(_item["ver_out"]):
        print u"|  " + str(i+1) + ". " + v

    print u"+-----------------------------------------+"
    print

    if platform.system() == "Windows":
        _sel_n = input_select_index((u"请输入序号：").encode("GB2312"),len(_item["ver_out"]))
    else:
        _sel_n = input_select_index(u"请输入序号：",len(_item["ver_out"]))

    if None == _sel_n:
        return None
    
    print u"已选择:",_item["ver_out"][_sel_n-1]
    return  e2l.get_fullpath(_git_root,_item["ver_out"][_sel_n-1])

def can_export_file(_filename,_bname,_cp_set):

    if "~" == _filename[:1]:
        return False
    if not e2l.is_excel_file(_filename):
        return False
    if None == _cp_set:
        return True

    if ("~" + _bname) in _cp_set: # 反向列表
        return False

    if "*" in _cp_set:    # 通配符，允许所有，通常和 反向列表 ~ 配合使用
        return True

    if _bname in _cp_set:
        return True

    return False
    

def do_export_version_folder(_doc_root,_ver_dir,_work_out_dir,_filter_file):

    _cp_set = None
 
    if isinstance(_filter_file,list):
        _cp_set = set()
        for _v in _filter_file:
            _cp_set.add(os.path.splitext(_v)[0])
        
        if len(_filter_file) == 0 :
            print u"‘f模式’ 下未选择任何文件！"
            raw_input("input any key to continue ... ")
            return
        else:
            print u"‘f模式’ 文件选择：",",".join(_filter_file)
    else: #elif isinstance(_filter_file,str) or isinstance(_filter_file,unicode):
        # 查找拷贝文件列表： 先 目标文件夹， 再 doc 文件夹
        if None == _filter_file:
            _filter_file = "server_copy_filter.py"
        _cp_list,_cp_path = find_copy_file_list(_filter_file,[_work_out_dir,_doc_root,tools_path])
        if None == _cp_list:
            print u"过滤列表文件：<无>"
        else:
            print u"过滤列表文件：",_cp_path
            _cp_set = set(_cp_list)
            

    # 开始拷贝文件到 doc 的 config 中
    _export_in_dir = os.path.join(_doc_root,"config")   # 导出工具的  输入目录
    e2l.makedirs(_export_in_dir)
    print u"拷贝excel文件:" + _ver_dir + " => " + _export_in_dir
    _cp_count = 0
    _deal_set = set()
    for _filename in os.listdir(_ver_dir):
        _bname = os.path.splitext(_filename)[0] # 去掉扩展名
        if can_export_file(_filename,_bname,_cp_set):
            print u"    %-40s ... " % (_filename),
            shutil.copyfile(os.path.join(_ver_dir,_filename),os.path.join(_export_in_dir,_filename))
            _cp_count = _cp_count + 1
            _deal_set.add(_bname)
            print u" ok!"

    print u"拷贝完成 " + str(_cp_count) + " 个文件!"

    # 开始导出
    print u"开始导出!" 

    _export_out_dir = os.path.join(_export_in_dir,"export_config")
    e2l.makedirs(_export_out_dir)
    _ret_flag = e2l.export_all(_export_in_dir,_export_out_dir,_deal_set)
    if _ret_flag != 0:
        return

    # 拷贝到目标文件夹 
    _cp_dest_dir = os.path.join(_work_out_dir,"skynet","game","config")
    print u"拷贝导出文件:" + _export_out_dir + " => " + _cp_dest_dir
    _cp_count = 0
    for _filename in os.listdir(_export_out_dir):
        _bname = os.path.splitext(_filename)[0] # 去掉扩展名
        if _bname in _deal_set:  # 之拷贝 本次 处理的： 在版本中，切在列表中
            print u"    %-40s ... " % (_filename),
            shutil.copyfile(os.path.join(_export_out_dir,_filename),os.path.join(_cp_dest_dir,_filename))
            _cp_count = _cp_count + 1
            print u" ok!"

    print u"拷贝完成 " + str(_cp_count) + " 个文件!"
    print
    raw_input("input any key to continue ... ")
    print    

# 处理版本文件夹 并导出
def export_version_folder(_item,_cmd_set):

    _doc_root = e2l.get_fullpath(rootPath,_item["doc_dir"])

    # 选版本文件夹
    _ver_dir = select_version_folder(_item,_cmd_set)
    if None == _ver_dir:
        return

    _filter_files = None
    if "f" in _cmd_set:     # f 模式 ：手动挑选文件
        _filter_files = select_files(_ver_dir)
        if _filter_files == None:
            return
    else:
        _filter_files = _item.get("filter")

    # 选 目标工作目录文件夹
    _work_out_dir = select_out_work_folder(_item)
    do_export_version_folder(_doc_root,_ver_dir,_work_out_dir,_filter_files)
            
def deal_default_select(_default_export):

    print
    print u"开始执行默认操作 ..."
    print

    if _default_export.has_key("ver_out"):
        _doc_root = e2l.get_fullpath(rootPath,_default_export["doc_dir"])
        _ver_dir = os.path.join(_doc_root,_default_export["cfg_dir"])

        # 输出 root 的相对路径 以 _doc_root 为准
        _git_root = _doc_root[:_doc_root.rfind(os.sep)]
        _work_out_dir = e2l.get_fullpath(_git_root,_default_export["ver_out"])

        do_export_version_folder(_doc_root,_ver_dir,_work_out_dir,_default_export.get("filter"))
    else:
        e2l.export_all(
                os.path.join(_default_export["doc_dir"] , "config"),
                os.path.join(_default_export["doc_dir"] , "config", "export_config"))
        raw_input("input any key to continue ... ")

# 参数 _items ： 选项列表 
# 注意控制台编码： chcp 936 , 否则乱码
def select_and_export_all(_items):

    #print sys.getdefaultencoding()
    #print "xxxxxxxxxxxxxxxdddddd:", eval("""[213,42,"ffdd"]""")

    print
    print u"+------------[项目列表]-------------------+"
    for i,item in enumerate(_items):
        print u"|  " + str(i+1) + ". " + item["desc"]

    print u"+-----------------------------------------+"
    print u"  说明: 输入数字选择; "
    print u"        前缀加 v 处理版本文件夹"
    print u"        前缀加 a 处理所有文件夹"
    print u"        前缀加 f 文件模式,可选择一个或多个文件"
    print
    if default_export_option != None and default_export_option.has_key("doc_dir"):
        print u"  默认操作："
        print u"    doc_dir：",default_export_option.get("doc_dir")
        print u"    cfg_dir：",default_export_option.get("cfg_dir")
        print u"    filter ：",default_export_option.get("filter")
        print u"    ver_out：",default_export_option.get("ver_out")
    print

    if len(_items) == 0:
        print
        print u"参数错误，项目列表为空!"
        print
        raw_input("input any key to continue ... ")
        return

    _cmd = ""
    _sel_n = 0
    while True:
        if platform.system() == "Windows":
            _sel = raw_input((u"请输入序号(输入 q 退出)：").encode("GB2312"))
        else:
            _sel = raw_input(u"请输入序号(输入 q 退出)：")

        if "" == _sel:
            if default_export_option == None or not default_export_option.has_key("doc_dir"):
                print u"放弃!"
                print
                return
            deal_default_select(default_export_option)
            return

        # 解析命令
        m = re.search(r'^([a-zA-Z]*)([0-9]*)$',_sel)
        if m == None:
            print u"错误的输入。请输入数字序号，或 v+数字序号(例如： v1)。"
            continue
        _cmd = m.group(1)
        if _cmd == "q":
            return

        if m.group(2) == None or m.group(2) == "":
            print u"未输入项目序号！"
            continue
            
        _sel_n = int(m.group(2))
        if _sel_n < 1 or _sel_n > len(_items):
            print u"项目序号超出范围！"
            continue

        _cmd_set = set()
        _err = False
        
        if "" == _cmd:
            print u"已选择:",_items[_sel_n - 1]["desc"]
            export_default(_items[_sel_n - 1],_cmd_set)
        else:
            for _c in _cmd:
                if "v" == _c or "a" == _c or "f" == _c:
                    _cmd_set.add(_c)
                else:
                    print u"前缀命令不正确！"
                    _err = True
                    break

            if not _err:
                print u"已选择:",_items[_sel_n - 1]["desc"]
                export_version_folder(_items[_sel_n - 1],_cmd_set)

        if _err:
            print u"前缀命令不正确！"
            continue

        break

        
 


