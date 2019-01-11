#!/bin/bash

date >> ~/log.txt

source ~/uranium/bin/activate

cd /home/user/git_files/GOSZAKUPKI/

Xvfb :1 -screen 0 1920x1080x24+32 -fbdir /var/tmp &

export DISPLAY=:1

python3 ~/git_files/GOSZAKUPKI/Main.py &>> ~/log.txt

date >> ~/log.txt
