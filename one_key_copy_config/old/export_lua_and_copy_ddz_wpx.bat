@echo off
SetLocal EnableDelayedExpansion

:: 设计目的，斗地主 和 欢乐捕鱼，bat脚本会是两个，
:: 不同的项目，可以选导出版本，是客户端还是服务器配置，目标路径

:: ------------------------------------------------ 要修改的配置 ↓
:: doc 文件夹的路径 , 一个项目只能是一个doc来源
set doc_dir=E:\JYHD\JyQipai_doc

:: tools的路径
set tools_dir=E:\JYHD\JyQipai_tools

:: 导出py脚本
set py_sprite=e2l_JyQipai_doc_lzm.py

:: 服务器 文件夹路径
set server_dir_name_1=E:\JYHD\JyQipai_server_dev\skynet\game\config
set server_dir_name_2=E:\JYHD\JyQipai_server_dev1\skynet\game\config

:: 客户端 文件夹路径
:: set client_dir_name_1=E:\JyQipai\JyQipai_server_dev\skynet\game\config
:: set client_dir_name_2=E:\JyQipai_copy\JyQipai_server_dev_copy1\skynet\game\config

:: ------------------------------------------------- 要修改的配置 ↑

:: -------------------------------------------------------------------------------- 选配置类型 ↓
:: 要拷贝的文件的txt文件
set need_copy_file_txt=copy_doc_for_server.txt
set config_type=1

:: 暂时只能用于服务器 ！！！
:: set /p config_type=------------拷贝服务器配置(1)，还是客户端配置(2)：

:: if %config_type%==1 (
:: 	set need_copy_file_txt=copy_doc_for_server.txt
:: ) else if %config_type%==2 (
:: 	set need_copy_file_txt=copy_doc_for_client.txt
:: ) else (
:: 	echo 请输入1 表示服务器配置 或者 2表示客户端配置
:: 	pause
:: 	goto :eof
:: )

:: ------------------------------------------------------------------------------- 选doc版本 ↓
:: doc 要导出的文件夹
set export_dir=config_debug
set /p version=---------请输入要导出的配置版本，输1是debug;输10.27表示config_10.27 :

if %version%==1 (
	if not exist %doc_dir%\config_debug (
		echo 不存在文件夹 %doc_dir%\config_debug
	)
) else (
	if not exist %doc_dir%\config_%version% (
		echo 不存在文件夹 %doc_dir%\config_%version%
		pause
		goto :eof
	)
	set export_dir=config_%version%
)

:: -------------------------------------------------------------------------------- 选目标路径 ↓
:: 导出后的文件，拷贝到的文件夹
::set tar_dir=XX

set /p tar_dir_type=------------输入拷贝到的目标路径，自己在代码中定义的(1-n)：
:: 如果是处理服务器配置
if %config_type%==1 (
	if not defined server_dir_name_%tar_dir_type% (
		echo ------未定义内置变量 server_dir_name_%tar_dir_type%
		pause
		goto :eof
	)
	for %%i in (%tar_dir_type%) do (
		set tar_dir=!server_dir_name_%%i!
	) 
) else if %config_type%==2 (
	if not defined client_dir_name_%tar_dir_type% (
		echo ------未定义内置变量 client_dir_name_%tar_dir_type%
		pause
		goto :eof
	)
	for %%i in (%tar_dir_type%) do (
		set tar_dir=!client_dir_name_%%i!
	)
)

:: --------------------------------------------------------------------------------

:: echo 333 %tar_dir%
:: echo %export_dir%
:: echo %doc_dir%\%export_dir%

echo ----

:: echo ------------------------------- 删除 doc 下的 config，/S表示删除目录树，/Q表示不询问
RMDIR /S /Q %doc_dir%\config
echo %doc_dir%\config ----- 路径删除成功

:: echo ------------------------------- 新创 doc config下的export_config
md %doc_dir%\config\export_config
echo %doc_dir%\config\export_config ----- 路径创建成功

echo ------------------------------- 拷贝文件到 doc config 中
:: 遍历配置的原始路径，
for /r %doc_dir%\%export_dir% %%i in (*) do (
	::echo %%i
	for /f "tokens=* delims= " %%f in (%~dp0%need_copy_file_txt%) do (
		
		if %doc_dir%\%export_dir%\%%f == %%i (
			echo 找到需要拷贝文件 %%i
			
			copy /Y %%i %doc_dir%\config
		)
		
	)
)

echo ------------------------------- 调用导出脚本 %tools_dir%\script\excel2lua\%py_sprite%
%tools_dir%\Python27\python.exe %tools_dir%\script\excel2lua\%py_sprite%


:: /s 表示包含目录树 /y表示 不询问
echo ------------------------------- 拷贝到目标 路径中 , %tar_dir%
xcopy %doc_dir%\config\export_config %tar_dir% /s /y


echo ------------------------操作完成！
pause>nul