#coding=utf-8

import sys
import lib.e2l_ui
sys.setdefaultencoding( "utf-8" )

ignore_files = [
u"*",
u"~act_ty_exchange_config.xlsx",
u"~act_ty_gifts_config.xlsx",
u"~act_ty_rank_config.xlsx",
u"~activity_fkzjd_config.xlsx",
u"~activity_ty_task_config.xlsx",
u"~banner_style_ui.xlsx",
u"~game_activity_config.xlsx",
u"~game_enter_btn_config.xlsx",
u"~game_module_config.xlsx",
u"~mini_game_config.xlsx",
u"~QIYE_shoping_config.xlsx"
]

params = [
    {
        "desc"    : u"★★★【 鲸鱼斗地主 】★★★",
        "doc_dir" : u"JyQipai_doc",
        "filter"  : ignore_files,
        "ver_out" : 
            [
                u"JyQipai_server_dev", # 和 doc 平行的文件夹 可以配置相对路径
                u"JyQipai_server_dev_copy",
            ],
    },
    {
        "desc"    : u"※※※【欢乐天天捕鱼】※※※",
        "doc_dir" : u"HuanLe_doc",
        "filter"  : ignore_files,
        "ver_out" : 
            [
                "HuanLe_server",
                "HuanLe_server_1",
            ]
    }
]

# 默认执行选项（一键爽）
lib.e2l_ui.set_default_export({
    "doc_dir" : u"JyQipai_doc",
    "cfg_dir" : u"config_debug",              # doc 仓库下 的 子文件夹
    "filter"  : ignore_files,
    "ver_out" : u"JyQipai_server_dev",
})

# doc 中需要优先显示的文件夹（注意： config_debug 不需要加，默认会最优先）
# lib.e2l_ui.add_custom_version_folder([
#     u"充值商城",
#     u"config_捕鱼数值测试",
#     u"config_IOS",
#     u"config_ios提审",
# ])

lib.e2l_ui.select_and_export_all(params)
