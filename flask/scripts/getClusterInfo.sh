#!/usr/bin/env bash

# Params
#
# ClusterName
#
# Return
#
# Построчную инфу об узлах

source /usr/lib/footloose-vpc/scripts/config.sh

cd "$CLUSTER_DIR"
NODENAME=$(cat "$1.yaml" | grep name | grep % | awk '{print $2}' | sed "s/%d//")
ignite ps | grep "$1-$NODENAME" | while read LINE; do echo $LINE; done
