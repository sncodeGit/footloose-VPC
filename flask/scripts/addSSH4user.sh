#!/usr/bin/env bash

# Params
#
# UserName SSHkey

source /usr/lib/footloose-vpc/scripts/config.sh

echo "$2" >> /home/"$1"/.ssh/authorized_keys
