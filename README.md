# KERMit

## Server

### Setup
To start up the server, follow this sequence of steps

#### 1. Activate the virtualenv and install dependencies for the project

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

#### 2. Set environmental variables

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

#### 3. Start the server

Starting the server is as simple as:
```
$ flask run
```

### Endpoints

#### I. Registration

To register a new user with their username and password, make a `POST` request to `/register` with the following
request body as json:
```
{
    "username": <username>,
    "password": <password>
}
```
If successful endpoint will return an access token and a refresh token for the user. Here is a sample response:
```
{
    "message": "User <username> was successfully created",
    "access_token": <token here>
    "refresh_token": <token here>
}
```
#### Login

To login with a username and password make a `POST` request to `/login`  with the following request 
body as JSON:
```
{
    "username": <username>,
    "password": <password>
}
```
If successful endpoint will return an access token and a refresh token for the user. The response
will be in the same format as the response from the registration endpoint.

For all other requests, access tokens will be required in the `Authorization` field of the request header. 
Set the field to `Bearer <access token here>`.

#### Puzzles

To get ALL puzzles for a specific user make a `GET` request to `/puzzles`. Note that the user doesn't have to be 
specified; it will be retrieved based on the submitted access token. Here is a sample response:

```
{
    "puzzles": [
        {
            "puzzle_id": 1,
            "completed": false,
            "difficulty": 0.5,
            "point_value": 90,
            "pieces": [ 
                ... // list of puzzle pieces (see example below)
            ],
            "players": [
                {
                    "username": "tester",
                    "id": 1
                }
            ]
        }
    ]
}
```

To see a specific puzzle, make a `GET` request to `/puzzles/<puzzle_id>/`, where `<puzzle_id>` is 
the id of the puzzle in the database. Here is an example response:

```
{
    "puzzle_id": 1,
    "completed": false,
    "difficulty": 0.5,
    "point_value": 90,
    "pieces": [
        {
            "x_coordinate": 0,
            "y_coordinate": 1,
            "static_piece": true,
            "value": 5
        },
        {
            "x_coordinate": 0,
            "y_coordinate": 2,
            "static_piece": true,
            "value": 4
        },
        // ... all other pieces....
    ],
    "players": [
        {
            "username": "tester",
            "id": 1
        },
        {
            "username": "anothertester",
            "id": 2
        }
    ]
}
```

To add a number to the puzzle, make a `POST` request to `/puzzles/<puzzle_id>/piece` with the following
request body as JSON:
```
{
    "x_coordinate": 0,
    "y_coordinate": 0,
    "value": 2
}
```
Here is a sample successful response:
```
{
    "message": "Successfully saved the submission of 2 at (0, 0) on puzzle_id 1 by user 'testuser'"
}
```

There are a number of possible requests that are invalid; responses to invalid requests
will have a `message` and `reason` field explaining what happened.

## Tests

### Unit Tests

To run unit tests:
```
$ (venv) python -m pytest ./tests/unit
```

### Integration Tests

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

(To be filled in more later)
https://github.com/oleg-agapov/flask-jwt-auth