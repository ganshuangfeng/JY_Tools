#!/bin/bash
#
#
if [ $# -eq 0 ]; then
	echo "give a parameter,please" && exit 1
fi

if [ -e ~/gitpull.log ]; then
	sudo rm -f ~/gitpull.log
else sudo touch ~/gitpull.log && sudo chmod 777 ~/gitpull.log
fi

for d in $(ls $1); do
	cd $1$d
	if [ $? -eq 0 ]; then
		git reset --hard HEAD && git pull --all && echo "$d success" &>> ~/gitpull.log		
		if [ $? -ne 0 ]; then
			echo "$d error" &>> ~/gitpull.log && echo "stop,$d error " && exit 2
		fi 
	else echo "file not exist" && exit 3
	fi
done

cat ~/gitpull.log
sudo rm -f ~/gitpull.log		
