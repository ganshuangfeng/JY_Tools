#coding=utf-8

import sys
import lib.e2l_ui
sys.setdefaultencoding( "utf-8" )

params = [
    {
        "desc"    : u"★★★ 休闲海外配置导出 ★★★",
        "doc_dir" : u"JyQipai_doc",
    },
]

lib.e2l_ui.select_and_export_all(params)
