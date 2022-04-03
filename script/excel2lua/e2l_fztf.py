# -*- coding: utf-8 -*- 
import os
import os.path
import xdrlib,sys
import xlrd
import types
import time

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
rootPath=rootPath[:rootPath.rfind(os.sep)]

#使用正斜杠 / 分割目录层次
#指定 excel 文件目录,文件夹下所有excel文件都将会被导出
# excel_dir= "../../makefunofzombie_doc/config"

# #指定导出的 lua 文件目录,所有导出的lua都被输出到此目录
# lua_dir = "../../makefunofzombie_resource/config"
excel_dir= rootPath+"/FZTF/FZTF_doc/config"

#指定导出的 lua 文件目录,所有导出的lua都被输出到此目录
lua_dir = rootPath+"/FZTF/FZTF_doc/config/export_config"



def cast_float(num):
    if int(num) == num:
        return "%d"%num
    return "%.6f"%num

    
    
def all_is_num(str):
    for ch in str:
        if (ch < '0' or ch > '9')and(ch != '.')and(ch != '-')and(ch != '+'):
            return False
            
    return True
    
def all_is_abc(str):
    for ch in str:
        if not ((ch <= 'Z' and ch >= 'A')\
        or (ch <= 'z' and ch >= 'a')):
            return False
    return True

#"2018/4/10 10:19:00"标准时间格式转换为时间戳
#必须一模一样，一字不差
def attempt_date_time(str):
    dl = len("2018/4/10 10:19:00")
    tl = len(str)
    if dl == tl:
        timestamp = 0
        try:
            timeArray = time.strptime(str, "%Y/%m/%d %H:%M:%S")
            timestamp = time.mktime(timeArray)
        except:
            return 0
        else:
            return int(timestamp)
    return 0

def cast_data(str):
    ret = str
    if type(str) in (type(u''),type('')):
        dtime = attempt_date_time(str)
        if dtime > 0:
            return "%d"%dtime
        str = str.replace("\n","")	
        i = str.find("|")
        if i >= 0:
            ret = str[0:i]
        
    elif type(str) == type(1.0):
        ret = cast_float(str)
    elif type(str) == type(1):
        ret = "%d"%str
    else:
        print "***\t" + str + "/t***\texcel data error"
        assert(0)
    return ret    
    # if type(ret) == type(u''):
        # print "***\t" + ret + "/t***\UnicodeEncode error"
        # assert(0)
    # else:
        # return ret

def mulit_data(data):
    '''多个数据的处理
        = 右边是字符串的时候检测添加""
        去掉换行符
    '''
    data = data.replace("\n","")
    
    l = 0
    r = 0
    lr = 0
    splitLStr = []
    splitRStr = []
    subStr = ""
    for idx in range(1,len(data)):
        ch = data[idx]
        if data[idx-1] == "=":
            l = idx
        if l > 0 and (ch == "," or ch == "}"):
            r = idx
        
        if l > 0 and r < 1:
            subStr += ch
            
        if r > 0:
        
            if not all_is_num(subStr) and subStr.find('"') < 0:
                splitLStr.append(data[lr:l])
                splitRStr.append(subStr)
                lr = r
            subStr = ""
            l = 0
            r = 0
            
    tail = data[lr:]
            
    i = 0
    lenght = len(splitLStr)
    str = ""
    while i < lenght:
        str += splitLStr[i] + '"' + splitRStr[i] + '"'
        i+=1
    str += tail

    return str
    
        
def cell_data(str):
    '''单元格数据处理,处理字符串值,多项数据'''
    data = cast_data(str)
    ii = data.find("*",0,1)
    if ii == 0:
		return '[[' + data[1:] + ']]'

    i = data.find(",")
    if i < 0:
        if not all_is_num(data):
            return '"' + data + '"'
        else:
            return data
    else:       
        data = "{" + data + "}"
        return mulit_data(data)



def tittle_data(str):
    '''表头数据处理,判断字符串还是是索引'''
    data = cast_data(str)
    if not all_is_num(data):
        return '"' + data + '"'
    else:
        return data

        
    
def level_t_str(lv):
    '''打印嵌套层数的制表符'''
    str = ""
    for i in range(1,lv):
        str += "\t"
    return str


def head_table_str(lv,content):
    '''打印lua表前括号部分'''
    str = content
    if all_is_num(str):
        str = level_t_str(lv) + "[" + content + "]=\n"\
        + level_t_str(lv) +  "{\n"
    else:
        str = level_t_str(lv) + content + "=\n"\
        + level_t_str(lv) +  "{\n"
    return str
 
 
def tail_table_str(lv):
    '''打印lua表后括号部分'''
    str = level_t_str(lv) + "},\n" 
    return str  
    


def is_has_lv_tittle(title_name_list):
    '''判断表头是否有* level *标志 将会把内部数据嵌入一层table'''
    idx = -1
    for tn in title_name_list:
        idx += 1
        if (tn).find("level") >= 0:
            return idx;
    return -1
    

def is_update_tittle(title_name_list,row_list):
    '''表头更新 如果 发现某一行第一格的内容和表头第一格一样 那么用这一行更新表头'''
    if title_name_list[0] == row_list[0]:
        return True
    return False
    

def expore_data(excel_name):

    ridx = excel_name.rfind('.')
    lidx = excel_name.rfind('/')
    real_file_name = excel_name[lidx+1:ridx]
    
    if real_file_name[0] == "~" :
        return 0
    
    #打印信息
    print real_file_name,"\n"
    
    
    
    lua_code_context = ""
    
    #lua表嵌套层数
    tabl_level = 1
    lua_code_context += "return {\n"
    
    book = xlrd.open_workbook(excel_name,encoding_override="utf-8")
    sheet_name_list = book.sheet_names()
    sheet_num = book.nsheets
    
    for sheet_idx in range(sheet_num):
        sheet = book.sheet_by_index(sheet_idx)
        nrows = sheet.nrows
        ncols = sheet.ncols
        sheet_name = sheet_name_list[sheet_idx]
        
        if nrows < 1 or len(cast_data(sheet_name)) < 1:
            '''跳过空的sheet 或者 被注释了的 sheet'''
            continue
            
        title_name_list = sheet.row_values(0)
        
        
        has_repeat_id = False
        id_map_data = []
         
        #创建映射数据            
        for row_idx in range(1,nrows):
            has_insert = False
            row_data = sheet.row_values(row_idx)
            #for map_data in id_map_data:
            #    if map_data[0] == row_data[0]:
            #        has_insert = True
            #        map_data.append(row_data)
                    
            if  not has_insert:
                data = []
                data.append(row_data[0])
                data.append(row_data)
                id_map_data.append(data)
               
        # print id_map_data
        
        
        tabl_level += 1
        lua_code_context += level_t_str(tabl_level)\
        + cast_data(sheet_name)\
        + "=\n" + level_t_str(tabl_level) + "{\n"
        
        for map_data in id_map_data:
            id = map_data[0]
            
            #抛弃行首为空的行
            if len(cast_data(id)) <= 0:
                continue
            elif is_update_tittle(title_name_list,map_data[1]):
                title_name_list=map_data[1]
                continue
            tabl_level += 1
            lua_code_context += head_table_str(tabl_level,cast_data(id))
            #lv_idx = is_has_lv_tittle(title_name_list)
            lv_idx = -1

            if len(map_data) > 2 or lv_idx >= 0:
                for idx in range(0,len(map_data)):
                
                    tabl_level += 1
                    if lv_idx >= 0:
                        lua_code_context += head_table_str(tabl_level,cell_data((map_data[idx][lv_idx])))
                    else:
                        lua_code_context += head_table_str(tabl_level,cast_data(idx))
                    
                    for col_idx in range(1,ncols):
                        #去除整列被注释的和单元格内容为空的
                        title_name = cast_data(title_name_list[col_idx])
                        cell_cont = cell_data((map_data[idx][col_idx]))
                        
                        if len(title_name) > 0 and len(cell_cont) > 0:
                            lua_code_context += level_t_str(tabl_level+1)\
                            + title_name + " = " + cell_cont + ",\n"
                            
                    lua_code_context += tail_table_str(tabl_level)
                    tabl_level -= 1
                
            else:
            
                for col_idx in range(0,ncols):
                    #去除整列被注释的和单元格内容为空的
                    title_name = cast_data(title_name_list[col_idx])
                    cell_cont = cell_data((map_data[1][col_idx]))
                    
                    if len(title_name) > 0 and len(cell_cont)>0:
                        lua_code_context += level_t_str(tabl_level+1)\
                        + title_name + " = " + cell_cont + ",\n"
                    
            
            lua_code_context += tail_table_str(tabl_level)
            tabl_level -= 1
            
        lua_code_context += tail_table_str(tabl_level) 
        tabl_level -= 1
        
    
    lua_code_context += "}"
    tabl_level -= 1
    
    ridx = excel_name.rfind('.')
    lidx = excel_name.rfind('/')
    lua_file_name = lua_dir + "/" + excel_name[lidx+1:ridx] + ".lua"
    try:
        lua_file = file(lua_file_name,"w")
        lua_file.write(lua_code_context)
        lua_file.close()
    except:
        print "\n*** " + lua_dir + " *** is open error,check is exist?\n"
        tabl_level = 1
    
    return tabl_level
    
    
    
    
if __name__=="__main__":
    flag = 0
    
    #1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for parent,dirnames,filenames in os.walk(excel_dir):
        for filename in filenames:
            if filename.rfind(".xls") > 0 or \
            filename.rfind(".xlsx") > 0:
                excel_name = excel_dir + "/" + filename
                flag += expore_data(excel_name)
                if flag > 0:
                    break
        if flag > 0:
            break
                    
    if flag == 0:
        print "\nexport to lua finish !!! \n"
    raw_input("input any key to continue ... ")
