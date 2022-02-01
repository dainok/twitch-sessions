# Automating Dynamic Lists for PANW firewalls

External Dynamic List (EDL) can be used to automate firewall policies on Palo Alto Networks firewalls. This Twitch session discussed how to create a simple Django application to do that.

## Install Django

Install Django into a Python environment (see S01E01):

~~~
pip install Django==4.0.1
~~~

## Create the Django application

Create the first Django project and an application within it:

~~~
django-admin startproject rrapp
cd rrapp
django-admin startapp edlprovider
./manage.py migrate
~~~

By default the database is a SQLite file stored under the Django root folder. The app must be loaded in the `settings.py` file stored in the `rrapp` folder:

~~~
INSTALLED_APPS = [
    ...
    "edlprovider",
]
~~~

Create the admin user:

~~~
./manage.py createsuperuser
~~~

## Modelling

In the simplest version of our application, we can expect that:

* an admin user is adding one or more EDL objects (list of IP addresses);
* an admin user is adding one or more IP addresses to one EDL object;
* eventually an expiration time can be set to each IP address;
* unexpired IP addresses will be available in a text list under a specific, non-guessable, URL.

In other words we have two objects:

* edl with ID, name, URL;
* IP with name, expiration date (optional), associated edl.

When the model is complete, we need to update the migration scripts and upgrade the database schema:

~~~
./manage.py makemigrations
./manage.py migrate
~~~

## Admin page

By default Django provides an admin page for each model. It can be anbled adding in the `admin.py` file:

~~~
admin.site.register(models.EDL)
admin.site.register(models.IPAddress)
~~~

Open the Django application using the URL `/admin`, add one EDL with at least one IP address.

## Printing EDLs

The `view.py` file is used to serve custom HTTP request. We need to print the content of each EDL if a GET is requesting the EDL id (slug). The URL is defined in the `rrapp/urls.py` file.

All IP addresses linked to a specific EDL are printed in text format if the expiration date is in the future.

## Starting the server

In the `settings.py` file you can configure Django to serve any client. This is an insecure configuration. Add `*` to the `ALLOWED_HOSTS`:

~~~
ALLOWED_HOSTS = ['*']
~~~

Start the application:

~~~
./manage.py runserver 0.0.0.0:8000
~~~

The Django application is now reachable. Use the `/admin` url and login with the superuser credentials created before.

## Using the EDL from a PANW firewall

Once an EDL is populated, it can be used as source or destination on ACLs.

EDL can be debugged with the following commands:

~~~
admin@fw> request system external-list stats type ip name EDL1
admin@fw> request system external-list show type ip name EDL1
admin@fw> request system external-list refresh type ip name EDL1
~~~

Last note: when an IP address is removed from an EDL, the session is not cleared. In other words the established sessions are maintained, new sessions are dropped.

A script should clear sessions related to expired IP addresses:

~~~
admin@fw> clear session all filter rule TestEDL1 destination 192.168.28.152
~~~

Mind also that firewall usually probes URL every 5 minutes, so the clear command should be executed 5 minutes after the expiration date. The web application should be extended to track requests and if they have been cleared.

## References

* [External Dynamic List](https://docs.paloaltonetworks.com/pan-os/10-1/pan-os-admin/policy/use-an-external-dynamic-list-in-policy/external-dynamic-list.html "External Dynamic List")
* [EDL provider app](https://github.com/dainok/rrapp/tree/main/rrapp/edlprovider "EDL provider app")
