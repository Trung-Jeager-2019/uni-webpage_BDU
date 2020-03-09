#!/bin/bash
# simple script to get this app running with Apache on Ubuntu 14.04

# upgrade the software packages
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get -y install apache2 libapache2-mod-wsgi-py3

# enable wsgi
sudo a2enmod wsgi

# install the needed python 3 and postgresql packages
sudo apt-get -y install python3-dev python3-pip python3-software-properties software-properties-common \
    postgresql-9.3 postgresql-server-dev-9.3

# start the postgresql service and create a user and database
sudo /etc/init.d/postgresql start &&\
    sudo -u postgres psql -c "CREATE USER comein WITH PASSWORD 'comein' CREATEDB;" &&\
    sudo -u postgres psql -c "CREATE DATABASE comein WITH OWNER comein"

# install flask and the necessary dependencies
sudo pip3 install Flask Flask-Login Flask-SQLAlchemy Flask-WTF Jinja2 SQLAlchemy\
    WTForms Werkzeug itsdangerous psycopg2 passlib

# populate the database
python3 db_create.py

# copy the apache conf file to the sites-available directory
sudo cp uni_web.conf /etc/apache2/sites-available/

# copy the website directory to /var/www
sudo cp -r /home/$USER/uni_web /var/www/uni_web

# create new group which has the current user and www-data as members
sudo groupadd web-content
sudo useradd -g web-content $USER
sudo useradd -g web-content www-data

# set the permissions so that the current user has write access and www-data has read access
# anyone outside the web-content group has no access
sudo chown -R $USER:web-content /var/www/html
find /var/www/html -type f -exec chmod 640 {} \;
find /var/www/html -type d -exec chmod 750 {} \;

# enable the uni_web website, disable the default website and restart apache
sudo a2ensite uni_web
sudo a2dissite 000-default
sudo service apache2 restart
