#  Isshoni Sudoku

A web-based Sudoku application built with Flask and React. The application allows users to play 
puzzles of selected difficulty.

This project makes use of the `py-sudoku` library to facilitate in generating and checking
Sudoku puzzles.

Created by **KERMit**

Group Members:
* Megan Frenkel (mmf2171)
* Riddhima Reddy Narravula (rrn2119)
* Emily Jin (ej2332)
* Kundan Guha (kg2632)

## Server - Flask

## I. Setup
To start up the server, follow this sequence of steps:

#### i. Activate the virtualenv and install dependencies for the project

All dependencies for the server can be found in `./server/requirements.txt`. Create a new virtual 
python environment and install the dependencies by following the commands below:
```
$ cd server
$ python3 -m virtualenv venv        # create the virtualenv
$ source venv/bin/activate          # activate virtualenv
$ pip install -r requirements.txt   # install all dependencies
```
This should complete without any errors. Nevertheless, some users have reported issues installing
`psycopg2` using pip in Mac OS (this package is the PostgreSQL database adapter for Python).
In the case that this happens, this [page](https://stackoverflow.com/a/42264168) 
provides a working solution.

#### ii. Set environmental variables

In order to run the server, you'll need to set a few environmental variables to tell Flask 
 what app to run and which database to use. The following environmental variables can be used for
 development.
```
$ export SECRET_KEY="supersecretkey"       
$ export APP_SETTINGS="server.config.DevelopmentConfig"         # configuration file to use
$ export FLASK_APP="server.py"                                  # where the flask app is launched
$ export FLASK_ENV="development"                                # sets environment to development 
$ export SQLALCHEMY_DATABASE_URI_DEV=<<URI for DB>>             # uri for the db
```

For production settings, add the environmental variables above, but change the following:
```
$ export APP_SETTINGS="server.config.ProductionConfig"
$ export FLASK_ENV="production"
$ export SQLALCHEMY_DATABASE_URI_PROD=<<URI for DB>> 
```

Two Heroku Postgres databases are setup for this project (one for dev and one for testing). Ask Meg for
the URI for these databases if you'd like to use them. You can setup any postgres database locally that you'd 
like though!
 
#### iii. Start the server

Start the flask server using gunicorn and evenlet:
```
$ gunicorn server:app -b localhost:5000 -k eventlet --log-level DEBUG
```
Setting the `log-level` as `DEBUG` is helpful in development, but not strictly necessary. This
will run the server on `localhost:5000`. Eventlet is necessary for providing support
for web-socket transports (default Flask development server only supports long-polling).

## II. Endpoints

Documentation of the backend API supporting this Sudoku application is 
available [here](https://documenter.getpostman.com/view/8320178/TVemA8kq) via Postman.

## III. Tests/Checks

When running the scripts outlined below, all test/coverage/style check results will be written to a file in 
`./reports/backend` under the corresponding folder.

### i. Unit Tests

To run unit tests:
```
$ (venv) ./bin/run_backend_tests.sh unit
```

### ii. Integration Tests

To run the integration test suite for the api, make sure to set the following
environmental variables: `SQLALCHEMY_DATABASE_URI_TEST`, `FLASK_APP`, `FLASK_ENV`. 

If you forget to set the `SQLALCHEMY_DATABASE_URI_TEST` correctly, you'll see this error message: 
`AttributeError: 'NoneType' object has no attribute 'drivername'`.

To run the tests:
```
$ (venv) ./bin/run_backend_tests.sh integration
```

To run both integration and unit tests at the same type, simply omit the specification of 
integration and unit:
```
$ (venv) ./bin/run_backend_tests.sh
```

### iii. Test Coverage

This project uses python's coverage tool to check test coverage. To run coverage:
```
$ (venv) ./bin/run_backend_coverage.sh <TEST-TYPE>
```
Where `<TEST-TYPE>` can be `unit`, `integration` or not specified (in this case it will run 
both test types) and determine coverage based on both.

### iv. Bug/Style Checker

This project uses pylint for style checking and bug finding. To run pylint:

```
$ (venv) ./bin/run_backend_bugs_style_check.sh 
```

### v. Manual Tests

The easiest way to manually the API is through Postman. You can easily generate an oauth2 token 
for testing by going to Google's Oauth 2.0 Playground 
[here](https://developers.google.com/oauthplayground/).

Make sure that in the first step, you authorize the following two APIs found under 
`Google Oauth2 API v2`:
```
* https://www.googleapis.com/auth/userinfo.email
* https://www.googleapis.com/auth/userinfo.profile
```
Once you clicked on "Authorize APIs" (you may also need to sign into Google) and have exchanged 
the authorization code for tokens, the access token field should automatically populate. 
You can use this access token for any requests made in Postman until the token expires.
