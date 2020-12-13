#!/usr/bin/env bash

# Params
#
# ClusterName SSHkey

source /usr/lib/footloose-vpc/scripts/config.sh

cd "$CLUSTER_DIR"
CLUSTER_NAME=$(cat "$1".yaml | grep name | head -1 | awk '{print $2}')
for node in $(footloose -c "$1".yaml show | awk '{print $1}' | sed '1d')
do
NODE_NAME=$(echo $node | sed -r "s/$CLUSTER_NAME-//")
footloose -c "$1".yaml ssh $NODE_NAME "echo $2 >> ~/.ssh/authorized_keys"
done