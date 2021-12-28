# Patching NTC Templates

## Configure git

~~~
git config --global user.email "andrea.dainese@pm.me"
git config --global user.name "Andrea Dainese"
~~~

## Fork, clone, update and merge lastest changes

Fork the [NTC-Templates GitHub repository](https://github.com/networktocode/ntc-templates) via web and clone the repositoy locally:

~~~
git clone https://github.com/dainok/ntc-templates
~~~

Add the original upstream:

~~~
git remote add upstream https://github.com/networktocode/ntc-templates
git remote -v
~~~

Update the local repository:

~~~
git fetch upstream
~~~

Merge latest changes:

~~~
git rebase upstream/master
~~~

## Make changes

Create a new branch:

~~~
git checkout -b fix_for_old_hp_procurve
~~~

Add/modify:

* templates: ntc_templates/templates/hp_procurve_show_mac-address.textfsm
* raw output: tests/hp_procurve/show_mac-address/hp_procurve_show_mac-address2.raw
* parsed output: tests/hp_procurve/show_mac-address/hp_procurve_show_mac-address2.yml

## Testing

Prepare Python virtual environment:

~~~
apt-get install python3-venv python3-pip
python3 -m venv venv
source .venv/bin/activate
pip install tox textfsm
~~~

Manual test with a simple Python script:

~~~
import textfsm
import json

template_file = 'ntc_templates/templates/hp_procurve_show_mac-address.textfsm'
raw_output = 'tests/hp_procurve/show_mac-address/hp_procurve_show_mac-address2.raw'

with open(template_file) as fd_t, open(raw_output) as fd_o:
	re_table = textfsm.TextFSM(fd_t)
	parsed_header = re_table.header
	parsed_output = re_table.ParseText(fd_o.read())

json.dumps(parsed_header)
json.dumps(parsed_output)
~~~

Or we can use ntc-templates libraries:

~~~
import yaml
from ntc_templates.parse import parse_output

platform = 'hp_procurve'
command = 'show mac-address'
raw_output_file = 'tests/hp_procurve/show_mac-address/hp_procurve_show_mac-address2.raw'
data = open(raw_output_file, 'r').read()
parsed_output = parse_output(platform=platform, command=command, data=data)

yaml.dump(parsed_output)
~~~

Final tests:

~~~
tox
~~~

You should get a 100% success.

## Commit and Pull Request

Add files, commit and create the pull request from the original repository.
