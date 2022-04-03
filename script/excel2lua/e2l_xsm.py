#coding=utf-8

import sys
import lib.e2l_ui
sys.setdefaultencoding( "utf-8" )

path_root_e = None
path_root_d = None

params = [
    {
        "desc"    : u"★★★【 鲸鱼斗地主 】★★★",
        "doc_dir" : u"JyQipai_doc",
        "ver_out" : 
            [
                u"JyQipai_server_dev", # 和 doc 平行的文件夹 可以配置相对路径
                u"JyQipai_server_next",
                u"JyQipai_server_next_next",
            ],
    },
    {
        "desc"    : u"※※※【欢乐天天捕鱼】※※※",
        "doc_dir" :  u"../Huanle/HuanLe_doc",
        "ver_out" : 
            [
                "HuanLe_server_dev",
                "HuanLe_server_next",
            ]
    },
]

# 默认执行选项（一键爽）
lib.e2l_ui.set_default_export({
    "doc_dir" : u"JyQipai_doc",
    "cfg_dir" : u"config_宝石迷阵",              # doc 仓库下 的 子文件夹
    # "filter"    : [
    #         u"tuoguan_duanwei_server.xlsx",
    #         #u"drive_game_equipment_server.xlsx",
    #         #u"drive_game_car_level_up_server.xlsx",
    #     ],
    "filter"  : u"server_copy_filter.py",
    #"ver_out" : u"Dongfeng_server2",
})

# doc 中需要优先显示的文件夹（注意： config_debug 不需要加，默认会最优先）
lib.e2l_ui.add_custom_version_folder([
#    u"config_IOS",
#    u"config_ios提审",
])

lib.e2l_ui.select_and_export_all(params)
