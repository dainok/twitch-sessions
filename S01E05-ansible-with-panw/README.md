# Anisble with PANW devices

## Install Ansible

Install a requred Python library:

~~~
pip install pan-os-python pan-python pandevice xmltodict requests requests_toolbelt
~~~

See the first episode (S01E01) then install PAN-OS Ansible collection:

~~~
ansible-galaxy collection install paloaltonetworks.panos
~~~

The `interpreter_python` on `ansible.cfg` file must point to the interpreter with the PanOS libraries installed.

## Sending operational commands

The module `panos_op` allows to send command to the firewall. The module translate the given command into XML and use the XML API. Some commands can fail so a best way is to specify commands using the XML syntax. The following command is failing:

~~~
cmd: 'show arp management' # Fails with "show -> arp has unexpected text."
~~~

The following command is working:

~~~
cmd: "<show><arp><entry name='management'/></arp></show>"
cmd_is_xml: true
~~~

The API browser, available on the Firewall using the `/api` URL can help to find out the right request. The above API is available at `/php/rest/browse.php/op::show::arp`.

## References

* [PAN-OS Ansible Collection](https://galaxy.ansible.com/paloaltonetworks/panos "PAN-OS Ansible Collection")
* [PAN-OS Ansible Collection Documentation](https://paloaltonetworks.github.io/pan-os-ansible/ "PAN-OS Ansible Collection Documentation")
* [PAN-OS XML API Labs with pan-python](http://api-lab.paloaltonetworks.com/ "PAN-OS XML API Labs with pan-python")
