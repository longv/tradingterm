#!/bin/bash
set -e

ROLE=$1

if [ "$ROLE" = "master" ]; then
    /opt/bitnami/scripts/spark/run.sh --master spark://spark-master:7077
elif [ "$ROLE" = "worker" ]; then
    /opt/bitnami/scripts/spark/run.sh --worker spark://spark-master:7077
else
    echo "Invalid role: $ROLE"
    exit 1
fi
