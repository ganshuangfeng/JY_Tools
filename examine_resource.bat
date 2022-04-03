 
@echo off

set python_cmd=%~d0%~p0Python27\python.exe
set script_file=%~d0%~p0script\compare2same\compare2same.py

%python_cmd% %script_file%
