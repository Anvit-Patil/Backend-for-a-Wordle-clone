# CPSC 449 - Project 4

Follow the steps to run process

### Authors
Group 18
Members:
- Ayush Bhardwaj (885866178)
- Ashley Thorlin ()
- Anvit Rajesh Patil ()
- Parva Parikh ()


## Setup Dependencies

- Python 3 (with pip)
- Quart
- SQLite 3
- Databases
- SQLAlchemy
- Foreman
- Quart-Schema
- HTTPie
- PyTest (including pytest-asyncio)
- Redis
- RQ
- HTTPX

Run the following commands to install all dependencies:
```
$ sudo apt update
$ sudo snap install httpie
$ sudo apt install --yes python3-pip ruby-foreman sqlite3
$ python3 -m pip install --upgrade quart[dotenv] click markupsafe Jinja2
$ python3 -m pip install sqlalchemy==1.4.41
$ python3 -m pip install databases[aiosqlite]
$ python3 -m pip install pytest pytest-asyncio
$ sudo apt install nginx
$ sudo apt install --yes nginx-extras
$ sudo apt install --yes python3-hiredis
$ python3 -m pip install rq
$ python3 -m pip install httpx

```
### Configuring Nginx File
#### Path (/etc/ngnix/sites-enabled/tutorial)

Configure the tutorial file  in the nginx server as shown below :

```

upstream backend {
	server 127.0.0.1:5100;
	server 127.0.0.1:5200;
	server 127.0.0.1:5300;
}

server {
      	listen 80;
      	listen [::]:80;

      	server_name tuffix-vm;

      	location / {
		auth_request /auth;
		proxy_pass http://backend;
      	}

		location = /auth {
			proxy_pass http://127.0.0.1:5000/user/login;
		}

		location /register {
			proxy_pass http://127.0.0.1:5000/user/register;
		}

		location /leaders {
			proxy_pass http://127.0.0.1:5400/leaderboard/players
		}

        location /game_register_urls{
            proxy_pass http://backend/game/register;
        }
}


```
#### Restart Nginx Service
After changing the tutorial file in nginx. Restart the server bhy follwing command:
```
$ sudo service nginx restart

```


### Configuring CronJob File




### Launching the App
Start the foreman to launch the App

```
$ foreman start

```

### Initializing the Database
to create database, Run the following command
```
$ ./bin/init.sh

```

### User Authentication Routes
#### Registering a new user
```
http POST http://localhost:5000/user/register username=<new username> password=<new password>
```

To Login Hit the following endpoint with username and password.
#### Logging In
```
http POST http://localhost:5000/user/login --auth <username>:<password>

```
It will return `{"authenticated": True}` if properly authenticated.


### Game Endpoints
#### Start a game
```
http --auth <username>:<password> POST http://localhost:5001/game/user/start username=<username>

```
This will only create a new game for the user. It will return the game ID, if successful.

#### List all active games
```
http --auth <username>:<password> GET http://localhost:5001/game/{username}/{game_id}
```
This lists all the game IDs of the active games of the user. Note that this only lists **active** games -- unfinished games that are below the 6 guess limit.

#### Guess a word
```
http --auth <username>:<password> POST http://localhost:5001/game/guess/ game_id=<game_id> guess_word=<guess_word> username=<username>
```
This Api checks whether the guess is correct or not.


Return JSON is in the form of:
```
{
  "guessesRemain": <Remaining_guess>,
  "isValid": <word_valid_or_not>,
  "correctWord": <correct_or_not>,
  "letterPosData": {
    "correctPosition": <list of position of correct letter>,
    "correctLetterWrongPos": <list of position of wrong letter>,
    "wrongLetter": <list of position of wrong letter>
  }
}
```




#### Register Client URLs
```
http://127.0.0.1:5400/game_register_urls [POST]
```
Allowing clients to register the URLs. Client URLs are stored in the database. 


## Redis Leaderboard Route
#### Populate Leaderboard with data
```
http://127.0.0.1:5400/leaderboard/add [POST]

```
Adds to the Leaderboard if game is won and calculates the score based on the number of guesses.

#### Top10 users
```
http GET http://127.0.0.1:5400/leaders

```
