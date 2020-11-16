#! /usr/bin/env python3

import os

root_pass = "123456"
myCmd = """ password=%s; \ """ %root_pass + """
correct=$(</etc/shadow awk -v user=root -F : 'user == $1 {print $2}') &&
prefix=${correct%"${correct#\$*\$*\$}"} &&
supplied=$(echo "$password" | perl -e '$_ = <STDIN>; chomp; print crypt($_, $ARGV[0])' "$prefix") &&
if [ "$supplied" = "$correct" ]; then echo Correct; else echo Incorrect; fi
"""

os.system(myCmd)