#!/usr/bin/env bash

# Params
#
# ClusterName
#
# Return
#
# Построчную инфу об узлах

source config.sh

cd "$CLUSTER_DIR"
NODENAME=$(cat "$1.yaml" | grep name | grep % | awk '{print $2}' | sed "s/%s//")
ignite ps | grep "$1-$NODENAME"
