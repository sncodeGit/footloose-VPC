#!/bin/bash

# $1 - root pass

password=$1;
correct=$(</etc/shadow awk -v user=root -F : 'user == $1 {print $2}');
prefix=${correct%"${correct#\$*\$*\$}"};
supplied=$(echo "$password" | perl -e '$_ = <STDIN>; chomp; print crypt($_, $ARGV[0])' "$prefix");

if [ "$supplied" = "$correct" ]
then
    echo Correct;
else
    echo Incorrect;
fi
