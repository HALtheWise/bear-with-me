# bear-with-me

**Creating authentic human connection in the modern world, via bear.**

By: Eric Miller, Toby Shapinsky, Jared Briskman 

Drawing inspiration from Oliver Steele's [bear-as-a-service](https://github.com/olinlibrary/bear-as-a-service).

## Overview
__Bear-with-me__ is a project of both software and social invention. Users call **The Bear**, who will connect their call with another random user, and give them a conversation prompt This provides an unexpected yet intentional interaction.

From a technical perspective, __bear-with-me__ is a python webapp integrated with twilio, and deployed on heroku.  

## Setup

#### Python
Use `pipenv` for dependency resolution. Installation instructions [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/#installing-pipenv).

Then simply use: 
```shell
$ pipenv install
``` 
#### Heroku
You will also need the heroku CLI. On Ubuntu: 
```shell
$ sudo snap install heroku --classic
```

#### Postgres
##### Install
For development, a local postgresql db is recommended. 
Install postgres:
```shell
$ sudo apt install postgresql
```
On Ubuntu, this installs authorized to a dedicated unix account 'postgres'.

##### Config
To create a separate account with a password:
```shell
$ sudo -i -u postgres
$ createuser <username>
$ createdb <dbname>
$ psql
# ALTER USER <username> WITH ENCRYPTED PASSWORD '<password>';
# GRANT ALL PRIVILEGES ON DATABASE <dbname> TO <username> ;
# \q 
```
You may also need to modify your `pg_hba.conf` to change local authentication from `peer` or `ident` to `md5`.
More information found [here](http://suite.opengeo.org/docs/latest/dataadmin/pgGettingStarted/firstconnect.html) and [here](https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e).

### Environment Variables
Copy `env.template` to `env.local` and edit the variables inside to match your configuration. 
To set the environment, simply `$ source env.local`. 

### Database Migrations

To change database schema, modify the models.py file, then commit the migration:
```shell
$ pipenv run flask db migrate -m "Changelog goes here"
```
Check the migration script, and apply with:
```shell
$ pipenv run flask db upgrade
```

To upgrade the production database, run:
```shell
$ heroku run upgrade
```

## Local Testing
Upon inital setup, you will need to upgrade the local db prior to use.
Make sure all secrets are set in `env.local`.

To start a local webserver, run:
```shell
$ pipenv run gunicorn app:app
```

### Deployment
Heroku server live at https://htl-p1-bear.herokuapp.com/
To deploy, push to the master branch on the heroku remote.
 
