#!/usr/bin/env bash

# Params
#
# ClusterName

source /usr/lib/footloose-vpc/scripts/config.sh

cd "$CLUSTER_DIR"
footloose -c "$1".yaml stop