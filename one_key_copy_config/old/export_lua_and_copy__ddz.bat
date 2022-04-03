@echo off
SetLocal EnableDelayedExpansion

:: ���Ŀ�ģ������� �� ���ֲ��㣬bat�ű�����������
:: ��ͬ����Ŀ������ѡ�����汾���ǿͻ��˻��Ƿ��������ã�Ŀ��·��

:: ------------------------------------------------ Ҫ�޸ĵ����� ��
:: doc �ļ��е�·�� , һ����Ŀֻ����һ��doc��Դ
set doc_dir=E:\JyQipai\JyQipai_doc

:: tools��·��
set tools_dir=E:\JyQipai\JyQipai_tools

:: ����py�ű�
set py_sprite=e2l.py

:: ������ �ļ���·��
set server_dir_name_1=E:\JyQipai\JyQipai_server_dev\skynet\game\config
set server_dir_name_2=E:\JyQipai_copy\JyQipai_server_dev_copy1\skynet\game\config

:: �ͻ��� �ļ���·��
set client_dir_name_1=E:\JyQipai\JyQipai_server_dev\skynet\game\config
set client_dir_name_2=E:\JyQipai_copy\JyQipai_server_dev_copy1\skynet\game\config

:: ------------------------------------------------- Ҫ�޸ĵ����� ��

:: -------------------------------------------------------------------------------- ѡ�������� ��
:: Ҫ�������ļ���txt�ļ�
set need_copy_file_txt=copy_doc_for_server.txt
set config_type=1

:: ��ʱֻ�����ڷ����� ������
:: set /p config_type=------------��������������(1)�����ǿͻ�������(2)��

:: if %config_type%==1 (
:: 	set need_copy_file_txt=copy_doc_for_server.txt
:: ) else if %config_type%==2 (
:: 	set need_copy_file_txt=copy_doc_for_client.txt
:: ) else (
:: 	echo ������1 ��ʾ���������� ���� 2��ʾ�ͻ�������
:: 	pause
:: 	goto :eof
:: )

:: ------------------------------------------------------------------------------- ѡdoc�汾 ��
:: doc Ҫ�������ļ���
set export_dir=config_debug
set /p version=---------������Ҫ���������ð汾����1��debug;��10.27��ʾconfig_10.27 :

if %version%==1 (
	if not exist %doc_dir%\config_debug (
		echo �������ļ��� %doc_dir%\config_debug
	)
) else (
	if not exist %doc_dir%\config_%version% (
		echo �������ļ��� %doc_dir%\config_%version%
		pause
		goto :eof
	)
	set export_dir=config_%version%
)

:: -------------------------------------------------------------------------------- ѡĿ��·�� ��
:: ��������ļ������������ļ���
::set tar_dir=XX

set /p tar_dir_type=------------���뿽������Ŀ��·�����Լ��ڴ����ж����(1-n)��
:: ����Ǵ������������
if %config_type%==1 (
	if not defined server_dir_name_%tar_dir_type% (
		echo ------δ�������ñ��� server_dir_name_%tar_dir_type%
		pause
		goto :eof
	)
	for %%i in (%tar_dir_type%) do (
		set tar_dir=!server_dir_name_%%i!
	) 
) else if %config_type%==2 (
	if not defined client_dir_name_%tar_dir_type% (
		echo ------δ�������ñ��� client_dir_name_%tar_dir_type%
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

:: echo ------------------------------- ɾ�� doc �µ� config��/S��ʾɾ��Ŀ¼����/Q��ʾ��ѯ��
RMDIR /S /Q %doc_dir%\config
echo %doc_dir%\config ----- ·��ɾ���ɹ�

:: echo ------------------------------- �´� doc config�µ�export_config
md %doc_dir%\config\export_config
echo %doc_dir%\config\export_config ----- ·�������ɹ�

echo ------------------------------- �����ļ��� doc config ��
:: �������õ�ԭʼ·����
for /r %doc_dir%\%export_dir% %%i in (*) do (
	::echo %%i
	for /f "tokens=* delims= " %%f in (%~dp0%need_copy_file_txt%) do (
		
		if %doc_dir%\%export_dir%\%%f == %%i (
			echo �ҵ���Ҫ�����ļ� %%i
			
			copy /Y %%i %doc_dir%\config
		)
		
	)
)

echo ------------------------------- ���õ����ű� %tools_dir%\script\excel2lua\%py_sprite%
%tools_dir%\Python27\python.exe %tools_dir%\script\excel2lua\%py_sprite%


:: /s ��ʾ����Ŀ¼�� /y��ʾ ��ѯ��
echo ------------------------------- ������Ŀ�� ·���� , %tar_dir%
xcopy %doc_dir%\config\export_config %tar_dir% /s /y


echo ------------------------������ɣ�
pause>nul