# KERMit

## Server

### Setup
To start up the server, follow this sequence of steps

##### 1. Activate the virtualenv and install dependencies for the project

All dependencies for the server can be found in `server/requirements.txt`. Create a new virtual python environment
and install the dependencies by following the commands below:
```
$ cd server
$ python3 -m virtualenv venv        # create the virtualenv
$ pip install -r requirements.txt   # install dependencies
```
This should complete without any errors. Nevertheless, some users have reported issues installing
`psycopg2` using pip in Mac OS (this package is the PostgreSQL database adapter for Python).
In the case that this happens, this [page](https://stackoverflow.com/a/42264168)  provides a working solution: 

##### 2. Set environmental variables

Make sure to set all the required environmental variables for the project. The settings below are for development.
```
$ export SECRET_KEY="supersecretkey"      
$ export JWT_SECRET_KEY="anothersecretkeyforjwt" 
$ export APP_SETTINGS="server.config.DevelopmentConfig"         # configuration file to use
$ export FLASK_APP="server.py"                                  # where the flask app is launched
$ export FLASK_ENV="development"                                # sets environment to development 
$ export SQLALCHEMY_DATABASE_URI_DEV=<<URI FOR DEV HEROKU DB>>  # uri for the heroku db (see below)
```

For production settings, change the following
```
$ export APP_SETTINGS="server.config.ProductionConfig"
$ export FLASK_ENV="production"
$ export SQLALCHEMY_DATABASE_URI_PROD=<<URI FOR PROD HEROKU DB>>
```

##### 3. Start the server

Starting the server is as simple as:
```
$ flask run
```

### Tests

#### Unit Tests

To run unit tests:
```
$ (venv) python -m pytest ./tests/unit
```

#### Integration Tests

To run the integration test suite for the api, make sure to set the following two
environmental variables: `SQLALCHEMY_DATABASE_URI_TEST` and `JWT_SECRET_KEY`. Note that
for the tests, the database and secret key can be whatever test information you'd like.

If you forget to set these environmental variables correct, you'll see this error message: 
`AttributeError: 'NoneType' object has no attribute 'drivername'`.

To run the tests:
```
$ (venv) cd server
$ (venv) python -m pytest ./tests/integration
```

### Sources

https://github.com/oleg-agapov/flask-jwt-auth