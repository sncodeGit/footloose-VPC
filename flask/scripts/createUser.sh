#!/usr/bin/env bash

# Params
#
# UserName

source /usr/lib/footloose-vpc/scripts/config.sh

adduser "$1" <<< "123afdgsklvJafsKAsAFgsjl 123afdgsklvJafsKAsAFgsjl"
mkdir /home/"$1"/.ssh
chown "$1":"$1" /home/"$1"/.ssh
touch /home/"$1"/.ssh/authorized_keys
chmod og-rwx /home/"$1"/.ssh/authorized_keys
chown "$1":"$1" /home/"$1"/.ssh/authorized_keys
