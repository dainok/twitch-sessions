# Ansible for networkers part 3

The `port-config.yml` file describes the intergaces that should be configured on the remote devices by the `playbook-2-port_provisioning.yml` playbook. The playbook must be called with an extra var:

~~~
./playbook-2-port_provisioning.yml -i hosts.py --extra-vars config_file=port-config.yml
~~~

Using this method it's possible to configure a small subset of interfaces, making the deploy faster.

The role `cisco_ios_qos`, based on what is defined in `qos-policies.yml`, configures generic class-map and generic policy-map for Voice and Internet.

The role `cisco_ios_port_provisioning`, based on what is defined in `port-config.yml`, configures devices interfaces:

1. for each device defined in `port-config.yml` file;
2. for each interface;
3. input and output policy-map are build for both Voice and Internet traffic.

To change interface values (Voice and/or Internet), interface must be disabled, and then enabled.

See previous episode also.
