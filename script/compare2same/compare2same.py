# -*- coding: utf-8 -*- 
import os
import os.path
import xdrlib,sys
import xlrd
import types
import time
import operator
import re

reload(sys)
sys.setdefaultencoding( "utf-8" )

#script root
def cur_File_Dir():
     
     path = sys.path[0]
     
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

rootPath=cur_File_Dir()
#git root
rootPath=rootPath[:rootPath.rfind(os.sep)]
rootPath=rootPath[:rootPath.rfind(os.sep)]
rootPath=rootPath[:rootPath.rfind(os.sep)]

#searh content
search_dirs=[rootPath+"/JyQiPai_art",\
# rootPath+"/JyQipai_client/1_code/Assets",\
]

#skip filename(xxx) suffix(*.xx) dir(xx/)
unsearch_items=[".git/",\
"*.docx",\
"*.ai",\
"*.txt",\
"*.pptx",\
".gitignore",\
"游戏界面/",\
"平面设计/",\
]

#ok file name chars
fc=r"[^a-z|A-Z|0-9|_]"

#file max size bytes
fmsz=500*1024

same_content_txt=[]
file_map={}
dir_map={}
same_content={}
error_filenames=[]
oversize_filenames=[]

def chkfilename(filename):
    for item in unsearch_items:
        lp = item.find("*.")
        rp = item.rfind("/")
        if lp >= 0:
            hz = item[2:]
            if filename.rfind(hz) == len(filename)-len(hz):
                return False
        elif rp < 0:
            if filename==item:
                return False
    return True

def chkdirname(dirname):
    for item in unsearch_items:
        rp = item.rfind("/")
        if rp >= 0:
            if dirname==item[:-1]:
                return False
    return True

def chkerrorfilename(filename,parent):
    p = filename.rfind(".")
    if p<=0:
        return False
    fn = filename[:p]
    if re.search(fc, fn, flags=0) != None:
        error_filenames.append(parent+"\\"+filename)
        return False
    return True

def chkfilesize(filename,parent):
	filePath = parent+"\\"+filename
	fsize = os.path.getsize(filePath)
	if fsize > fmsz:
		fss = "%.2fKB"%(fsize/float(1024))
		oversize_filenames.append(filePath+" - "+fss)

	
def search_all():
    tag = "\\:@"

    for search_dir in search_dirs:
        
        for parent,dirnames,filenames in os.walk(search_dir):
            
            #skip dir
            ok_dirs=[]
            for dirname in dirnames:
                if chkdirname(dirname):
                    ok_dirs.append(dirname)
            dirnames[:]=ok_dirs

            #all file
            for filename in filenames:

                if chkfilename(filename):
                    chkerrorfilename(filename,parent)
                    chkfilesize(filename,parent)
					
                    num = file_map.get(filename,0)
                    file_map[filename]=num+1
                    if num==2:
                        same_content[filename+"-"+("%d"%(num-1))]=file_map[filename+tag]+"\\"+filename
                        same_content[filename+"-"+("%d"%(num))]=parent+"\\"+filename
                    elif num>2:
                        same_content[filename+"-"+("%d"%(num))]=parent+"\\"+filename
                    file_map[filename+tag]=parent

                # for dirname in dirnames:
                #     num = dir_map.get(dirname,0)
                #     dir_map[dirname]=num+1
                #     same_content[dirname+"-"+("%d"%num)]=parent+"\\"+dirname

def sortedDictValues1(adict):
    keys = adict.keys()
    keys.sort()
    return map (adict.get,keys)

if __name__=="__main__":
    search_all()
    m=sortedDictValues1(same_content)

    print( "FILE NAME REPETITION LIST:" )
    for i in (m):
        print "\n",i

    print( "\nFILE NAME ERROR LIST :" )
    for x in error_filenames:
        print "\n",x
		
    print( "\nFILE NAME OVER SIZE LIST :" )
    for o in oversize_filenames:
        print "\n",o
    print( "\ncheck finish" )
    raw_input("input any key to continue ... ")


