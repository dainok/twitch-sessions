#!/usr/bin/env python3

import yaml, json

with open('hosts', 'r') as fd:
    hosts = yaml.load(fd, Loader=yaml.FullLoader)

print(json.dumps(hosts, sort_keys=True, indent=4, separators=(',', ':')))
