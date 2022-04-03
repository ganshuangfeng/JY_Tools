#coding=utf-8
import os
import os.path
import xdrlib,sys
import xlrd
import types
import time
import e2l

reload(sys)
sys.setdefaultencoding( "utf-8" )
    
if __name__=="__main__":
    
    e2l.export_all(sys.argv[1],sys.argv[2])
    raw_input("input any key to continue ... ")
    
