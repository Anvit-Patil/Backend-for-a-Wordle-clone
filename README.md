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
<p>1. Clone the repository</p>

```sh
git clone https://github.com/vudiep411/cpsc449-wordle-backend.git
```
<p>2. cd into the root directory</p>

```sh
cd cpsc449-wordle-backend/
```
<p>3. Install libraries needed</p>

```sh
./bin/requirements.sh
```
<p>4. Setting up the database</p>

```sh
./bin/init.sh
```
<p>5. Start the server with foreman</p>

```sh
foreman start
```

<p>6. Start redis server</p>

```sh
./redis.sh
```
<br/>

### Configuring Nginx File
#### Path (/etc/ngnix/sites-enabled/tutorial.txt)

To utilize the Nginx file we must set it up by 'cd /etc/nginx/sites-enabled' and then 'sudo "${EDITOR:-vi}" tutorial' (as described here: https://ubuntu.com/tutorials/install-and-configure-nginx#4-setting-up-virtual-host) into the Linux terminal. The second part will allow us to use the Linux terminal to edit the contents of the tutorial file which hosts the configuration of our Nginx settings. The named 'tutorial' Nginx configuration file and directories may need to be created before hand, see (https://ubuntu.com/tutorials/install-and-configure-nginx#1-overview) for more details on this process. See this (https://nginx.org/en/docs/http/ngx_http_core_module.html#directives) for explanations of Nginx configuration properties including ones like 'server_name.'
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
}
```
#### Restart Nginx Service
After configuration is done restart the the nginx service.
```
$ sudo service nginx restart

```

### Launching the App
Use the following command to start the app.( 3 game service, 1 leaderboard service and 1 user service will start)
```
$ foreman start

```

### Initializing the Database
Before running the app, run the following command to initialize the database and populate the table.
```
$ ./bin/init.sh

```

### Retrying Failed Jobs
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


> ⚠ The development server for User service will be started at http://127.0.0.1:5000/ <br/>
> ⚠ The 3 development servers for Game service will be started at <br/>
http://127.0.0.1:5100/  <br/>
http://127.0.0.1:5200/  <br/>
http://127.0.0.1:5300/  <br/>
> ⚠ Leaderboard service will be started at http://127.0.0.1:5400/ <br/>

To access leaderboard data through nginx, visit http://tuffix-vm/leaders

## Documentation

<p>After starting the server with foreman start, go to http://127.0.0.1:5000/docs, http://127.0.0.1:5100/docs, and http://127.0.0.1:5400/docs for all REST API routes example</p>
