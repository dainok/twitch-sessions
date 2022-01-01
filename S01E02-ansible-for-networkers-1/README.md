# Ansible for networkers part 1

## Install Ansible

Install `sshpass` package:

~~~
sudo apt-get install sshpass
~~~

Then install Ansible:

~~~
python3 -m venv venv
source venv/bin/activate
pip3 install wheel
pip3 install ansible==5.1.0 paramiko==2.9.1
~~~

Install additional modules:

~~~
ansible-galaxy collection list
ansible-galaxy collection install cisco.ios
~~~

## Cisco router configuration

The lab is build on EVE-NG but you can use any Cisco router. Configure it as following:

~~~
hostname R1
no ip domain lookup
ip domain name example.com
username admin privilege 15 password 0 cisco
crypto key generate rsa modulus 1024
ip ssh version 2
interface Ethernet0
 ip address dhcp
line vty 0 4
 login local
 transport input ssh
~~~

## Testing reachability

Testing that the router is reachable:

~~~
ping -c3 192.168.28.129
~~~

Try to access via SSH:

~~~
ssh admin@192.168.28.129
~~~

With older IOS version you can get a key exchange error:

~~~
Unable to negotiate with 192.168.28.129 port 22: no matching key exchange method found. Their offer: diffie-hellman-group-exchange-sha1,diffie-hellman-group14-sha1,diffie-hellman-group1-sha1
~~~

In that case force an old and insecure key exchange method:

~~~
ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 admin@192.168.28.129
~~~

## Ansible inventory

See attaches `hosts` file and customize it.

Test inventory and hosts connectivity:

~~~
ansible -i hosts all -m ping
~~~

Print facts:

~~~
ansible -i hosts all -m ansible.builtin.setup
ansible -i hosts all -m ansible.builtin.setup -m ansible.builtin.gather_facts
~~~

Also see `playbook-5-debug-all-vars.yml` and check how the output changes with or without `gather_facts`.

## Ansible playbooks

Test attached playbooks:

~~~
ansible-playbook --diff -i hosts playbook-1-config-diff.yml
ansible-playbook -i hosts playbook-2-provisioning.yml
ansible-playbook -i hosts playbook-3-provisioning.yml
ansible-playbook -i hosts playbook-4-provisioning.yml -C
ansible-playbook -i hosts playbook-4-provisioning.yml
ansible-playbook -i hosts playbook-4-provisioning.yml --tags nonex
~~~

## Create reusable roles

See under the `roles` directory and create new role structure:

~~~
ansible-galaxy init roles/cisco_ios_time_config
~~~
