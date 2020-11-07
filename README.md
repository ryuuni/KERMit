# KERMit

## Server - Flask API

### Setup
To start up the server, follow this sequence of steps

#### 1. Activate the virtualenv and install dependencies for the project

All dependencies for the server can be found in `./server/requirements.txt`. Create a new virtual python environment
and install the dependencies by following the commands below:
```
$ cd server
$ python3 -m virtualenv venv        # create the virtualenv
$ pip install -r requirements.txt   # install all dependencies
```
This should complete without any errors. Nevertheless, some users have reported issues installing
`psycopg2` using pip in Mac OS (this package is the PostgreSQL database adapter for Python).
In the case that this happens, this [page](https://stackoverflow.com/a/42264168)  provides a working solution.

#### 2. Set environmental variables

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
 
#### 3. Start the server

Starting the Flask server is as simple as issuing the following command
from the `./server` directory:
```
$ flask run
```

### Endpoints

#### I. Registration

This API relies on Google Oauth2 tokens for authentication and each request requires that the Oauth2 token be specified
in the request header. For example, in a curl command:
```
--header 'Authorization: Bearer <TOKEN HERE>
```

To register a new user with their username and password, make a `POST` request to `/register`. For user registration,
the API will ask Google for user information such as their first and last name and email address to store in the
backend database for the user, alongside the unique Google identifier for the person and a custom identifier for
this application. Subsequent requests match the requesting person with their application user based on the unique 
Google identifer.

If successful, the endpoint will return a message like the following:
```
{
    "message": "User Megan Frenkel was successfully registered"
}
```

To join a puzzle, make a `POST` request to the `/puzzles/<puzzle_id>` endpoint. Upon success, you will see
a message like:

```
{
    'message': "Successfully added Megan Frenkel (id = 1) to puzzle with id 2."
}
````

#### II. Puzzles

To get ALL puzzles for a specific user make a `GET` request to `/puzzles`. Note that the user doesn't have to be 
specified; it will be retrieved based on the submitted access token in the header. Here is a sample response:

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
                    "id": 2,
                    "first_name": "Megan",
                    "last_name": "Frenkel",
                    "email": "mmf2171@columbia.edu"
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
            "id": 2,
            "first_name": "Megan",
            "last_name": "Frenkel",
            "email": "mmf2171@columbia.edu"
        }
    ]
}
```

To get the solution to a puzzle and see any discrepancies between the player puzzle and the solution,
make a `GET` request to the `/puzzles/<puzzle_id>/solution` endpoint. If successful, you should see
a response that looks like:

```
{
    "solved_puzzle": {
        "puzzle_id": null,
        "completed": true,
        "difficulty": 0.5,
        "point_value": 90,
        "pieces": [
            {
                "x_coordinate": 0,
                "y_coordinate": 0,
                "static_piece": true,
                "value": 1
            },
            ... other pieces go here....  
        ],
    "discrepancy": [
        {
            "x_coordinate": 0,
            "y_coordinate": 0
        },
            ... all other discrepancies...
.       ]
    }

```

#### IV. Puzzle Pieces

To add a number to the puzzle, make a `POST` request to `/puzzles/<puzzle_id>/piece` (specifying the value 
for `puzzle_id`) with the following request body as JSON:
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
    "message": "Successfully saved the submission of 2 at (0, 0) on puzzle_id 1 by Megan Frenkel (id = 2)"
}
```

There are a number of possible requests that are invalid; responses to invalid requests
will have a `message` and `reason` field explaining what happened.

## Tests

### Unit Tests

To run unit tests:
```
$ (venv) cd server
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

### Manual Tests

The easiest way to manually the API is through Postman. You can easily generate an oauth2 token for testing
by going to Google's Oauth 2.0 Playground [here](https://developers.google.com/oauthplayground/).

Make sure that in the first step, you authorize the following two APIs found under `Google Oauth2 API v2`:
```
* https://www.googleapis.com/auth/userinfo.email
* https://www.googleapis.com/auth/userinfo.profile
```
Once you clicked on "Authorize APIs" (you may also need to sign into Google) and have exchanged the authorization
code for tokens, the access token field should automatically populate. You can use this access token for any requests 
made in Postman until the token expires.

### Sources

(To be filled in more later) 