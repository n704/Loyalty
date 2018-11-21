# Loyalty

## building

`docker-compose build`

## runing
`docker-compose up`

## test

Enter the container and run `./manage.py test`

##Code

This consist of 2 services 

* python 
* Node

Python service expose it public url for booking while private url from `node` is only avaialble in docker enviroment and visiable from outside.

## Working
on building 5 user and 5 rooms are created and working on these. room as id 1 to 5 similarly for rooms

## Env
Enviroment variblae are stored in `.env` file both services.
