#!/usr/bin/env bash

# Params
#
# ClusterName SSHkey

source config.sh

cd "$CLUSTER_DIR"
CLUSTER_NAME=$(cat footloose.yaml | grep name | head -1 | awk '{print $2}')
for node in $(footloose show | awk '{print $1}' | sed '1d')
do
NODE_NAME=$(echo $node | sed -r "s/$CLUSTER_NAME-//")
KEY_STR_NUM=$(footloose ssh $NODE_NAME "cat ~/.ssh/authorized_keys | grep -n $2" 2> /dev/null | cut -d ':' -f 1)
footloose ssh $NODE_NAME "sed -i "${KEY_STR_NUM}d" ~/.ssh/authorized_keys"
done