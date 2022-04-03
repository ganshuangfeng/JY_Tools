#coding=utf-8

import sys
import lib.e2l_ui
sys.setdefaultencoding( "utf-8" )

params = [
    {
        "desc"    : u"★★★【 鲸鱼斗地主 】★★★",
        "doc_dir" : u"JyQipai_doc",
        "ver_out" : 
            [
                u"JyQipai_server_dev", # 和 doc 平行的文件夹 可以配置相对路径
                u"../JyQipai_copy/JyQipai_server_dev_copy1"
            ],
    },
    {
        "desc"    : u"※※※【欢乐天天捕鱼】※※※",
        "doc_dir" : u"E:\HuanLe_server\HuanLe_doc",
        "ver_out" : 
            [
                "HuanLe_server"
            ]
    },
    {
        "desc"    : u"※※※【欢乐天天捕鱼-海外版】※※※",
        "doc_dir" : u"E:\HuanLe_server\HuanLe_Haiwai_server_Doc",
		"filter"  : u"server_copy_filter_huanle_haiwai.py",
        "ver_out" : 
            [
                "HuanLe_Haiwai_server"
            ]
    },
	{
        "desc"    : u"※※※【休闲游戏domino-海外版】※※※",
        "doc_dir" : u"E:\\xiuxian_haiwai\XiuXian_Haiwai_client_Doc",
		"filter"  : u"server_copy_filter_xiuxian_haiwai.py",
        "ver_out" : 
            [
                u"Xiuxian_Haiwai_server",
				u"Xiuxian_Haiwai_server_copy",
				u"Xiuxian_Haiwai_server_copy_2",
            ]
    },
    {
        "desc"    : u"-----【放置】-----",
        "doc_dir" : u"E:\FZTF\FZTF_doc",
        "filter"  : u"server_copy_filter_fztf.py",
        "ver_out" : 
            [
                "FZTF_server"
            ]
    },
]

# 默认执行选项（一键爽）
#lib.e2l_ui.set_default_export({
#    "doc_dir" : u"E:\HuanLe_server\HuanLe_Haiwai_server_Doc",
#    "cfg_dir" : u"config_Release",              # doc 仓库下 的 子文件夹
    # "filter"    : [
    #         u"tuoguan_duanwei_server.xlsx",
    #         #u"drive_game_equipment_server.xlsx",
    #         #u"drive_game_car_level_up_server.xlsx",
    #     ],
    #"filter"  : u"server_copy_filter.py",
    #"ver_out" : u"Dongfeng_server2",
#    "ver_out" : u"HuanLe_Haiwai_server",
#})


lib.e2l_ui.add_custom_version_folder([
    # u"config_捕鱼数值测试",
    # u"config_IOS",
    # u"config_ios",
    # u"config_ios提审",
])

lib.e2l_ui.select_and_export_all(params)
