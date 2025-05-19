# gymbudsapi

Backend API for GymBuds (built with FastAPI), handles any HTTP requests from the front end and any CRUD operations necessary for interacting with the database.

# Technologies Used + Packages used

## Technology

- FastAPI : Backend Web Framework
- PostgreSQL : Database Type

## Packages

Python (FastAPI Backend Packages):

fastapi
uvicorn
pydantic
sqlalchemy
alembic [migrations]
asyncpg/psycopg2
databases
bcrypt or passlib
pyjwt [auth]
python-dotenv
supabase, gotrue, storage3, supafunc
openai [deepseek]
requests
sendgrid [email sending]

# Backend Dependencies

- Any version of Python3.0 or higher
- PgAdmin and PostgreSQL
  - If running locally you would need to change the env to match a local database, we will provide you with a proper env where this is not needed
- Poetry (pip3 install poetry)
  - This is our package manager this ensures you do not need a specific version of python and all packages installed are a specific compatible version
- ngrok (see below)

# Steps to install and run

## Postgres Setup [if local]

install pgadmin and postgresql

## Pre-load of system

#### Open up a zsh or terminal

-Set up our system using: `poetry install`

-You need to get to latest alembic migration: `poetry run alembic upgrade head` [Only done if you are on local database]

## Running our system

#### Open up a zsh or terminal

Get our system running <br>
`poetry run uvicorn main:app`

#### Open up a SEPERATE zsh or terminal

You will need to run our backend with a tunneling service [ngrok] <br>
https://dashboard.ngrok.com/ <br>
command : `poetry run ngrok http 8000` <br>
This will give you a link that you can use in the front-end-env

# Our Deployment process

- For the backend, we utilized AWS Ec2 to cloud host our server
