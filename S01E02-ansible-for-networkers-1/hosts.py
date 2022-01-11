#!/usr/bin/env python3

import yaml, json

hosts = """
_meta:
  hostvars:
    r1.example.com:
      ansible_host: 192.168.28.129
      ansible_password: cisco
      ansible_user: admin
cisco_ios:
  hosts:
  - r1.example.com
  vars:    
    ansible_connection: ansible.netcommon.network_cli
    ansible_network_os: cisco.ios.ios
"""

hosts = yaml.safe_load(hosts)

print(json.dumps(hosts, sort_keys=True, indent=4, separators=(',', ':')))
