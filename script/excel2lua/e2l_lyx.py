#coding=utf-8

import sys
import lib.e2l_ui
sys.setdefaultencoding( "utf-8" )

path_root_d = None

if sys.platform == "win32":
    path_root_d = "D:/"
else:
    path_root_d = "/home/hare/shares/D/"

params = [
    {
        "desc"    : u"★★★【 鲸鱼斗地主 】★★★",
        "doc_dir" : u"JyQipai_doc",
        "ver_out" : 
            [
                u"JyQipai_server_dev", # 和 doc 平行的文件夹 可以配置相对路径
                u"JyQipai_server_dev2",
                u"JyQipai_server_dev3",
                path_root_d + u"work/JyQipai/JyQipai_server_dev",
                path_root_d + u"mytest/tmp_server"
            ],
    },
    {
        "desc"    : u"※※※【欢乐天天捕鱼】※※※",
        "doc_dir" : path_root_d + u"work/HuanLe/HuanLe_doc",
        "ver_out" : 
            [
                "HuanLe_server",
                "HuanLe_server2",
                "HuanLe_server3",
                "HuanLe_server_aliyun",
                path_root_d + "mytest/tmp_server"
            ]
    },
    {
        "desc"    : u"囍囍囍【海外】囍囍囍",
        "doc_dir" : path_root_d + u"work/Xiuxian_Haiwai/XiuXian_Haiwai_client_Doc",
        "filter"  : u"server_copy_filter_haiwai_lyx.py",
        "ver_out" : 
            [
                "Xiuxian_Haiwai_server",
                "Xiuxian_Haiwai_server2",
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
    "ver_out" : path_root_d + u"mytest/tmp_server",
})

# doc 中需要优先显示的文件夹（注意： config_debug 不需要加，默认会最优先）
lib.e2l_ui.add_custom_version_folder([
    u"config_新游戏",
    # u"config_IOS",
    # u"config_ios提审",
])

lib.e2l_ui.select_and_export_all(params)
