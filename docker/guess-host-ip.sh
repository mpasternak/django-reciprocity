#!/bin/bash -e

export POSSIBLE_IP=$(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+')

if [ "x$POSSIBLE_IP" == "x" ]; then
    export POSSIBLE_IP=$(getent hosts host.docker.internal | awk '{print $1 }')
fi

if [ "x$POSSIBLE_IP" == "x" ]; then
    echo "host IP not available, cannot continue";
    exit 1;
fi

echo "$POSSIBLE_IP host.docker.internal" >> /etc/hosts

cat /etc/hosts
