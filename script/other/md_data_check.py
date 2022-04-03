# -*- coding: utf-8 -*- 
# 检查埋点数据的基本问题
# 用法：
#     将 hlby-md/jy-md 数据库中的 game_client_click 表 按 v,ts,sn 排序 导出到excel，例如：
#             select * from game_client_click where time >= '2020-10-20 00:00:0' order by v,ts,sn
#     将excel放到 仓库doc/config中
# 

import os
import os.path
import xdrlib,sys
import xlrd
import types
import time
import json
import copy

reload(sys)
sys.setdefaultencoding( "utf-8" )

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
rootPath=rootPath[:rootPath.rfind(os.sep)]

#使用正斜杠 / 分割目录层次
#指定 excel 文件目录,文件夹下所有excel文件都将会被导出
# excel_dir= "../../makefunofzombie_doc/config"

# #指定导出的 lua 文件目录,所有导出的lua都被输出到此目录
# lua_dir = "../../makefunofzombie_resource/config"
excel_dir= rootPath+"/JyQipai_doc/config"

#指定导出的 lua 文件目录,所有导出的lua都被输出到此目录
lua_dir = rootPath+"/JyQipai_doc/config/export_config"


def inc_map_count(_map,_key):
    _map[_key] = _map[_key] + 1 if _map.has_key(_key) else 1

def inc_direct_count(_direct_stat,_src,_dest,_name):
    
    if _direct_stat.has_key(_src):
        if not _direct_stat[_src].has_key(_dest):
            _direct_stat[_src][_dest] = {}
        inc_map_count(_direct_stat[_src][_dest],_name)
    else:
        _direct_stat[_src] = {_dest:{_name:1}}

def write_text_file(_file,_text):
    f = open(_file,"w")
    f.write(_text)
    f.close()

def write_map_count(_map,_file,_col_title):    
    direct_stat_path = (lua_dir + "/" + _file).decode('utf-8')
    print "write " + direct_stat_path + " ..."
    csv_str_rows = [_col_title]
    for k,v in _map.items():
        csv_str_rows.append("{0},{1}".format(k,v))
    write_text_file(direct_stat_path,"\n".join(csv_str_rows).encode("gb2312"))  
    print direct_stat_path + " write ok!"  

# 埋点过滤器：只处理这里的点
md_filter = {
0:"启动",99:"<空>",100:"结束",  # 特殊点
#1:"首次启动", # 第一次启动app（注意是第一次启动） 
#2:"更新完成", # 更新完成
#3:"连接成功", # 服务器连接成功
#4:"异常断线", # 服务器异常断线
#5:"连接中断", # 服务器连接中断或者被踢掉
#6:"回到前台", # 回到前台
#7:"退到后台", # 退到后台
8:"微信登录", # 点击微信登录
9:"游客登录", # 点击游客登录
10:"手机登录", # 点击手机登录
11:"一键修复", # 点击一键修复
12:"联系客服", # 点击联系客服
13:"短信验证码", # 获取短信验证码
#14:"图片验证码", # 获取图片验证码
15:"手机号", # 输入手机号完成
16:"短信验证码", # 输入短信验证码完成
17:"手机:确定登录", # 手机登录界面：点击确定登录
18:"手机:点击关闭", # 手机登录界面：点击关闭
#19:"游客登录请求", # 游客登录请求
#20:"微信登录请求", # 微信登录请求
#21:"手机登录请求", # 手机登录请求
22:"登录失败", # 登录失败.
23:"登录成功", # 登录成功（加载完毕，进入大厅）
}

# md_filter = {
# 0:"启动",99:"<空>",100:"结束",  # 特殊点
# 1:"首次启动", # 第一次启动app（注意是第一次启动） 
# 2:"更新完成", # 更新完成
# 3:"连接成功", # 服务器连接成功
# 4:"异常断线", # 服务器异常断线
# 5:"连接中断", # 服务器连接中断或者被踢掉
# 6:"回到前台", # 回到前台
# 7:"退到后台", # 退到后台
# 8:"微信登录", # 点击微信登录
# 9:"游客登录", # 点击游客登录
# 10:"手机登录", # 点击手机登录
# 11:"一键修复", # 点击一键修复
# 12:"联系客服", # 点击联系客服
# 13:"短信验证码", # 获取短信验证码
# 14:"图片验证码", # 获取图片验证码
# 15:"手机号", # 输入手机号完成
# 16:"短信验证码", # 输入短信验证码完成
# 17:"手机:确定登录", # 手机登录界面：点击确定登录
# 18:"手机:点击关闭", # 手机登录界面：点击关闭
# 19:"游客登录请求", # 游客登录请求
# 20:"微信登录请求", # 微信登录请求
# 21:"手机登录请求", # 手机登录请求
# 22:"登录失败", # 登录失败.
# 23:"登录成功", # 登录成功（加载完毕，进入大厅）
# }    

# 处理一组埋点数据：替换为中文
def deal_md_record_tran(_md_data):

    # 替换为中文
    mdd_len = len(_md_data)
    for i in range(0,mdd_len):
        _md_data[i] = "%03d-%s" % ( _md_data[i] ,md_filter[_md_data[i]])


# 处理一组埋点数据：处理过滤器 和 删除连续空位
def deal_md_record_clean(_md_data):

    # 处理过滤器
    mdd_len = len(_md_data)
    for i in range(mdd_len-1,-1,-1):
        if not md_filter.has_key(_md_data[i]):

            del _md_data[i]

            # 删除 连续的空缺位
            if i > 0 and _md_data[i-1]==99 and len(_md_data) >= i and _md_data[i]==99:
                del _md_data[i]

def is_same_md_data(_data_prepare,_d):
    if len(_data_prepare) == 0:
        return False
    if _data_prepare[-1]["v"] != _d["v"]:
        return False
    if _data_prepare[-1]["ts"] != _d["ts"]:
        return False

    return True

def write_log_data(_file,_name,_log_data):
    # _direct_stat 写入 csv  
    direct_log_path = (lua_dir + "/" + _file + "_" + _name + ".csv").decode('utf-8')
    print "write " + direct_log_path + " ...",
    write_text_file(direct_log_path,("设备v,时间戳ts,原始埋点,处理埋点\n" + "\n".join(_log_data)).encode("gb2312"))
    print "ok!"

def write_direct_stat(_file,_name,_direct_stat):
    # _direct_stat 写入 csv  
    direct_stat_path = (lua_dir + "/" + _file + "_" + _name + ".csv").decode('utf-8')
    print "write " + direct_stat_path + " ...",
    csv_str_rows = ["源点,目标点,数量,数量(去重)"]
    for k,v in _direct_stat.items():
        for k2,v2 in v.items():
            csv_str_rows.append("{0},{1},{2},{3}".format(k,k2,v2["count"],v2["num"]))
    write_text_file(direct_stat_path,"\n".join(csv_str_rows).encode("gb2312"))
    print "ok!"

def log_md_data_row(_d,_deal_d):

    _md_strs = []
    for i in range(0,len(_d["md_vec"])):
        _md_strs.append(str(_d["md_vec"][i]))

    _md_strs_deal = []
    for i in range(0,len(_deal_d)):
        _md_strs_deal.append(str(_deal_d[i]))

    return "{},{},{},{}".format(_d["v"],_d["ts"],"|".join(_md_strs),"|".join(_md_strs_deal))

# 检查数据： 注意，此前必须按 v,ts,sn 排序过    
def check_data(_file,_rows):
    row_count = len(_rows)

    print "data count:",row_count

    # 预处理，将埋点数据转换为   开始、埋点、空缺、结束  的标准埋点数组
    # 数组  [{v=,ts=,md_vec=[埋点数组]},。。。]
    # 特殊埋点：0 开始, 99 空洞,  100 结束
    #           -1 ： 需要剔除（处理过程中 临时使用）
    data_prepare = []

    log_data_str = []

    last_sn = -1

    # 结束一条记录 时  进行的处理
    def done_md_record():
        data_prepare[-1]["md_vec"].append(100)
        _full_data = copy.deepcopy(data_prepare[-1])
        deal_md_record_clean(data_prepare[-1]["md_vec"])
        log_data_str.append(log_md_data_row(_full_data,data_prepare[-1]["md_vec"]))
        deal_md_record_tran(data_prepare[-1]["md_vec"])

    for i in range(0,row_count):
        d = _rows[i] 

        jdata = json.loads(d["d"])

        cur_d = None
        if not is_same_md_data(data_prepare,d):

            # 新的数据开始

            if len(data_prepare) > 0:
               done_md_record()

            cur_d = {
                "v":d["v"],
                "ts": d["ts"],
                "md_vec":[0] # 开始
            }
            if int(d["sn"]) > 1:
                cur_d["md_vec"].append(99)  # 有缺失

            data_prepare.append(cur_d)
            
        else:
            cur_d = data_prepare[-1]

            if int(d["sn"]) > (last_sn+1):
                cur_d["md_vec"].append(99)  # 有缺失

        #插入 埋点数据
        jdata = json.loads(d["d"])
        if d["t"] == "A":
            for i2 in range(0,len(jdata)):
                cur_d["md_vec"].append(int(jdata[i2]))
        else:
            cur_d["md_vec"].append(-1)

        last_sn = int(d["sn"])

    # 最后一个的结束处理
    if len(data_prepare) > 0:
        done_md_record()

    # write_text_file(lua_dir + "/debug_info.txt",json.dumps(data_prepare,indent=4))

    # 埋点数据 跳转统计
    direct_stat = {} # 源 => {目标 => {count=数量,num=去重后的数量}} ； 
    #                去重数量：去掉同一次启动 app 中重复点（起点 重点相同）
    for i in range(0,len(data_prepare)):
        cur_d = data_prepare[i] 

        add_md_pair = {} # 去除重复
        for i2 in range(0,len(cur_d["md_vec"])-1):

            inc_direct_count(direct_stat,cur_d["md_vec"][i2],cur_d["md_vec"][i2+1],"count")

            if add_md_pair.has_key(cur_d["md_vec"][i2]) and add_md_pair[cur_d["md_vec"][i2]].has_key(cur_d["md_vec"][i2+1]):
                continue
            inc_direct_count(direct_stat,cur_d["md_vec"][i2],cur_d["md_vec"][i2+1],"num")

            if not add_md_pair.has_key(cur_d["md_vec"][i2]):
                add_md_pair[cur_d["md_vec"][i2]] = {}
            add_md_pair[cur_d["md_vec"][i2]][cur_d["md_vec"][i2+1]] = True

    # 写文件

    _file = os.path.splitext(_file)[0]

    # 写入 csv  
    write_direct_stat(_file,"走向",direct_stat)

    # 写入 日志记录 csv
    write_log_data(_file,"记录",log_data_str)
        

def deal_data(_file,excel_name):

    ridx = excel_name.rfind('.')
    lidx = excel_name.rfind('/')
    real_file_name = excel_name[lidx+1:ridx]
    
    if real_file_name[0] == "~" :
        return 0
    
    #打印信息
    print "load file '", real_file_name , "' ... ",
    
    
    
    lua_code_context = ""
    
    #lua表嵌套层数
    tabl_level = 1
    lua_code_context += "return {\n"
    
    book = xlrd.open_workbook(excel_name,encoding_override="utf-8")
    sheet_name_list = book.sheet_names()
    sheet_num = book.nsheets

    print "ok\n"
    
    for sheet_idx in range(sheet_num):
        sheet = book.sheet_by_index(sheet_idx)
        nrows = sheet.nrows
        ncols = sheet.ncols
        sheet_name = sheet_name_list[sheet_idx]
        
        #if nrows < 1 or len(cast_data(sheet_name)) < 1:
        #    '''跳过空的sheet 或者 被注释了的 sheet'''
        #    continue
            
        title_name_list = sheet.row_values(0)
        #print "-- title --"
        #print title_name_list
        
        rows_data = [] # 行数据集合
         
        #创建映射数据            
        for row_idx in range(1,nrows):
            has_insert = False
            tmp_row_data = sheet.row_values(row_idx)
            row_data = {}
            for col in range(0,len(title_name_list)):
                row_data[title_name_list[col]] = tmp_row_data[col]
            rows_data.append(row_data)

            # if (row_idx % 10000) == 0:
            #     print "read row data count:",row_idx

        print "deal data start..."
        check_data(_file,rows_data)

    return 0
    
    
if __name__=="__main__":
    flag = 0
    
    #1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for parent,dirnames,filenames in os.walk(excel_dir):
        for filename in filenames:
            if filename.rfind(".xls") > 0 or \
            filename.rfind(".xlsx") > 0:
                excel_name = excel_dir + "/" + filename
                flag += deal_data(filename,excel_name)
                if flag > 0:
                    break
        if flag > 0:
            break
                    
    if flag == 0:
        print "\ndeal finish !!! \n"
    raw_input("input any key to continue ... ")
