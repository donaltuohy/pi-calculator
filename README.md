# pi-calculator
Calculate Pi


This project has two parts:

1. Server
2. Worker

## Server 

The server uses the flask library to accept requests. The only endpoint is `/calculate`. 

The server has a list of worker addresses and loops through these to check if they are healthy by sending a ping request. Once it has decided which workers are healthy, it divides out the work to each of the healthy workers.

## Worker

The worker can be spun up multiple times and when a server sends it a request, it is given a `start`, `end` and a `precision`. It uses the  [Bailey–Borwein–Plouffe formula](https://en.wikipedia.org/wiki/Bailey%E2%80%93Borwein%E2%80%93Plouffe_formula) to converge on the value of pi.


Running locally

To run this project locally, you can use the `docker-compose.yml` file.

Install docker compose and run the following command from the root of this repo: 

```
docker-compose up --remove-orphans --build 
```

To test it out, send a request with a json body:

```
curl --location --request POST 'http://localhost:5000/calculate' \
--header 'Content-Type: application/json' \
--data-raw '{
    "n":30,
    "x": 5000
}'
```