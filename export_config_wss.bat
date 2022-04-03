 
@echo off
chcp 936

set python_cmd=%~d0%~p0Python27\python.exe
set script_file=%~d0%~p0script\excel2lua\e2l_wss.py

%python_cmd% %script_file%
