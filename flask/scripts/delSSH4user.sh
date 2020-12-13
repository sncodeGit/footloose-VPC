#!/usr/bin/env bash

# Params
#
# UserName SSHkey

source /usr/lib/footloose-vpc/scripts/config.sh

KEY_STR_NUM=$(cat /home/"$1"/.ssh/authorized_keys | grep -n "$2" | cut -d ':' -f 1)
sed -i "${KEY_STR_NUM}d" /home/"$1"/.ssh/authorized_keys
