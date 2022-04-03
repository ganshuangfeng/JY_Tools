#!C:\Python27\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'Cheetah==2.4.4','console_scripts','cheetah-compile'
__requires__ = 'Cheetah==2.4.4'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('Cheetah==2.4.4', 'console_scripts', 'cheetah-compile')()
    )
