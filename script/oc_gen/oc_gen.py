#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#第一步:首先生成一个500位的数组 驼峰类型的元素 用作文件名 eg:AsdfdfGsd
# import random

# import string

# first = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# second = "abcdefghijklmnopqrstuvwxyz"
# number = "345"
# index = 0
# array = []
# for i in range(500):
#     final=(random.choice(first))
#     index = random.randint(3, 5)
#     for i in range(index):
#         final+=(random.choice(second))
#     final += (random.choice(first))
#     for i in range(index):
#         final+=(random.choice(second))
#     array.append(final)


# print (array)

#第二步:
#用上边生成的数组来创建对应的.h和.m文件
# -*- coding: utf-8 -*-
import random
import os
import string
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

################

total_context_file_h = open(rootPath + '/export/ChangleYouCommon.h', 'w')
total_context_file_h.write('//\n//  ChangleYouCommon.h\n//  tuzi\n\n//  create by changleyou.\n//  Copyright ©  changleyou corp. All rights reserved.\n//\n\n')
total_context_file_h.write(
'''
#import <UIKit/UIKit.h>

''')

total_context_file_m = open(rootPath + '/export/ChangleYouCommon.m', 'w')
total_context_file_m.write('//\n//  ChangleYouCommon.m\n//  tuzi\n\n//  create by changleyou.\n//  Copyright ©  changleyou corp. All rights reserved.\n//\n\n')
total_context_file_m.write(
'''
#import "ChangleYouCommon.h"

@interface ChangleYouCommonViewController()

 @end

@implementation ChangleYouCommonViewController

- (ChangleYouCommonViewController *)init { 

    self = [super init];
''')

#创建.h文件
def text_createH(fileNmae,msg,msg1,propertyNumber,methodArray,msg3):
    full_path = rootPath + '/export/' + fileNmae + '.h'
    file = open(full_path, 'w')
    file.write('//\n//  '+fileNmae+'.h\n//  tuzi\n\n//  create by changleyou.\n//  Copyright ©  changleyou corp. All rights reserved.\n//\n\n')
    file.write(msg)
    file.write(msg1)
    propryNameArray = []
    for index in range(1,propertyNumber):
        propryNameArray.append(random.choice(array))
    propryNameArray = list(set(propryNameArray))
    for propertyName in propryNameArray:
        file.write('@property(nonatomic,strong)'+random.choice(classArray)+' * '+propertyName+';\n')
    file.write('\n\n')
    for methodName in methodArray:
        file.write('- (void)pushTo'+methodName+'VC:(NSDictionary *)info;\n')
    file.write(msg3)
    file.close()
    print('Done')
#创建.m文件
def text_createM(fileNmae,msg,msg1,methodArray,msg3):
    full_path = rootPath + '/export/' + fileNmae + '.m'
    file = open(full_path, 'w')
    file.write('//\n//  '+fileNmae+'.m\n//  tuzi\n\n//  create by changleyou.\n//  Copyright ©  changleyou corp. All rights reserved.\n//\n\n')
    file.write(msg)
    file.write(msg1)
    for methodName in methodArray:
        file.write('- (void)pushTo'+methodName+'VC:(NSDictionary *)info\n{\n\n  NSMutableArray *array = [NSMutableArray array];\n')
        number = random.randint(3, 10)
        for i in range(1,number):
            file.write('  [array addObject:@"'+random.choice(array)+'"];\n')
        file.write('\n}\n\n')

        # 在 ChangleYouCommon.m 加入调用代码
        total_context_file_m.write("""
    {oname} * ptr{oname}_{methodname} = [[{oname} alloc] init];
    NSDictionary *_info_{oname}_{methodname} = [[NSDictionary alloc] init];
    if (_info_{oname}_{methodname})
    {{
        [ptr{oname}_{methodname} pushTo{methodname}VC:_info_{oname}_{methodname}];
    }}
""".format(oname=fileNmae,methodname=methodName))

    file.write(msg3)
    file.close()

    print(fileNmae + ' Done.')

classArray = ['NSString','UILabel','NSDictionary','NSData','UIScrollView','UIView']
array = ['Ungated','Denumerable','Campanology','Saddletree','Tarry','Cleidoic','Ullage','Maradi','Guttula','Chuckwalla','Sonlike','Vojvodina','Malapportionment','Genealogical','Heathrow','Famished','Respective','Evader','Assuasive','Taxability','Lattin','Elf','Astronomer','Scrotitis','Colossus','Laius','Uncharitable','Scandisk','Achitophel','Indulgency','Pounce','Wolfess','Penna','Flaxy','Ichnite','Telosyndesis','Bywalk','Imploration','Watercress','Beechen','Antibusing','Martinet']
array = list(set(array))

for name in array:
    number = random.randint(3, 10)
    methodArray = []
    for i in range(1,5):
        methodArray.append(random.choice(array))
    methodArray = list(set(methodArray))#数组去重
    text_createH(name+'ViewController', '#import <UIKit/UIKit.h>\n','@interface '+name+ 'ViewController:'+ 'UIViewController\n\n',number,methodArray,'\n\n@end')
    text_createM(name+'ViewController', '#import "'+name+'ViewController.h"\n\n' '@interface '+ name+'ViewController()\n\n @end\n\n','@implementation '+name+'ViewController\n\n- (void)viewDidLoad { \n\n [super viewDidLoad];\n\n}\n\n',methodArray,'\n\n@end')

    total_context_file_h.write('#import "'+name+'ViewController.h"\n')


total_context_file_h.write(
'''

@interface ChangleYouCommonViewController:UIViewController

- (ChangleYouCommonViewController *)init;
@end

''')
total_context_file_m.write('\n    return self;\n}\n@end\n')

total_context_file_m.close()
total_context_file_h.close()
