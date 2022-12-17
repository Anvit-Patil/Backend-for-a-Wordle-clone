# CPSC 449 Group 18 Project 4
<p><b>Group Member:</b> Ashley Thorlin, Anvit Patil, Ayush Bhardwaj, Parva Parikh</p>

## Setup
### Requirements
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
- Run-one

## Installations
<p>1. cd into the root directory</p>

```sh
cd cpsc449-wordle-backend/
```
<p>2. Install libraries needed</p>

```sh
./bin/requirements.sh
```
<p>3. Setting up the database</p>

```sh
./bin/init.sh
```
<p>4. Start the server with foreman</p>

```sh
foreman start
```

<p>5. Start redis server</p>

```sh
./redis.sh
```
<br/>

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


#### Retrying Failed Jobs
Cron Jobs help us to schedule any job in ubuntu as per our requiremnets. Here, we are setting that for every 10 minutes whichever job that are queued in rq queue, has been failed due to some issue in leaderboard service can be pushed again to leaderboard service so that the failed jobs can be retried again.
<br/>
Run this command in terminal
<br/>
```
crontab -e
```
<br/>
This will open editor where we can configure our crontab.
<br/>
Then paste this command
<br/>

```
*/10 * * * * run-one rq requeue --all --queue default
```
<br/>
Here run-one helps us to run just one instance of a command and its args at a time

<br/>
<br/>


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



> ⚠ The development server for User service will be started at http://127.0.0.1:5000/ <br/>
> ⚠ The 3 development servers for Game service will be started at <br/>
http://127.0.0.1:5100/  <br/>
http://127.0.0.1:5200/  <br/>
http://127.0.0.1:5300/  <br/>
> ⚠ Leaderboard service will be started at http://127.0.0.1:5400/ <br/>

To access leaderboard data through nginx, visit http://tuffix-vm/leaders

## Documentation

<p>After starting the server with foreman start, go to http://127.0.0.1:5000/docs, http://127.0.0.1:5100/docs, and http://127.0.0.1:5400/docs for all REST API routes example</p>
