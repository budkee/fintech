# Payment System

This repository is an recreational implementation of an connection system using SQLAlchemy and Flask

First, you'll have to build the image of the application `trab-lbd`, with the following command:
````sh
docker build -t trab-lbd .
````
Then, to run the app, you can choose between a postgres's or a mysql's stack, then run: 
````sh
docker compose -f mysql.yml up
````
or 
````sh
docker compose -f postgres.yml up
````
- if you don't want to follow the logs in the terminal, you can add the `-d` parameter, like this:
````sh
docker compose -f postgres.yml up -d
````

To stop the application, run:
````sh
docker compose -f postgres.yml up
````

Or if you want to delete all the composition and its data to start over, run:
````sh
docker compose -f postgres.yml down
````
