#!/usr/bin/env bash

# Params
#
# ClusterName

source /usr/lib/footloose-vpc/scripts/config.sh

cd "$CLUSTER_DIR"

CLUSTER_NAME=$(yq e ".cluster.name" "$1".yaml)
NODE_NAME=$(yq e ".machines" "$1".yaml | grep name | awk {'print $2'})
NODE_NAME="${CLUSTER_NAME}-${NODE_NAME}"
MACHINES_COUNT=$(yq e ".machines" "$1.yaml" | grep count | awk {'print $3'})
for ((i=0; i < ${MACHINES_COUNT}; i++))
do
    NOW_NODE=$(echo "${NODE_NAME//%d/${i}}")
    ignite stop "$NOW_NODE"
done

