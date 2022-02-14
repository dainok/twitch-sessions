#!/bin/bash

IMAGES=$(docker images | awk '{ print $3 }'| tail -n+2)
if [ "$IMAGES" == "" ]; then
	exit
fi
docker rmi $IMAGES &> /dev/null
