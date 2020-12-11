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
footloose ssh $NODE_NAME "echo $2 >> ~/.ssh/authorized_keys"
done