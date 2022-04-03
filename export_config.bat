
 
@echo off

set python_cmd=%~d0%~p0Python27\python.exe
set script_file=%~d0%~p0script\excel2lua\e2l.py

%python_cmd% %script_file%
