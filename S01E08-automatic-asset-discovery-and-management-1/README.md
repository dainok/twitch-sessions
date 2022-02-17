# Automatic asset discovery and management part 1

## Installing Nautobot (docker)

Review `nautobot/local.env` configuration file.

~~~
cd nautobot
docker-compose --env-file local.env up -d
docker-compose logs -t -f
~~~

Login using the port `8080` using the user `admin` with password `admin`.

In the `nautobot-with-plugins` folder, you can find a configuration example to build a custom Nautobot Docker image including plugins.

## Installing Snipe IT (docker)

Review `snipeit/local.env` configuration file.

~~~
cd snipeit
docker-compose --env-file local.env up -d
docker-compose logs -t -f
~~~

Open the port `8090` and complete the setup.

## Installing NetBox (docker)

Review `netbox/*.env` configuration files.

~~~
git clone https://github.com/netbox-community/netbox-docker
cd netbox-docker
cat << EOF > docker-compose.override.yml
version: '3.4'
services:
  netbox:
    ports:
      - 8080:8080
EOF
docker-compose up -d
docker-compose logs -t -f
~~~

## Installing RRapp NetDoc (local)

Prepare the environment:

~~~
sudo apt-get install -y git libmariadbclient-dev gcc python3-dev python3-venv
git clone https://github.com/dainok/rrapp
python3 -m venv rrapp/.venv
source rrapp/.venv/bin/activate
pip install wheel
pip install -r rrapp/requirements.txt
pip install -r rrapp/requirements-dev.txt
~~~

Configure RRapp:

~~~
cd rrapp
git submodule update --init ntc-templates
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
~~~

Start RRapp:

~~~
./manage.py runserver 0.0.0.0:8000
~~~
