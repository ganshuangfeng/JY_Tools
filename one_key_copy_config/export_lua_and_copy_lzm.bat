@echo off

chcp 936

set py_sprite=e2l_lzm.py

set tools_dir=%~d0%~p0\..

%tools_dir%\Python27\python.exe %tools_dir%\script\excel2lua\%py_sprite%
