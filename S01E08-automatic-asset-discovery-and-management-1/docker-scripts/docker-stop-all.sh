#!/bin/bash

CONTAINERS=$(docker ps -a | tail -n+2 | cut -d" " -f1)
if [ "$CONTAINERS" == "" ]; then
	exit
fi
docker stop $CONTAINERS
