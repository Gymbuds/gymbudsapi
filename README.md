# gymbudsapi

Backend API for GymBuds

# postgres set up db
install pgadmin and postgresql

# poetry

-set up your poetry using: poetry install
-if you need to install new packages do: poetry add [package name]
-if you make changes to models: poetry run alembic revision --autogenerate -m

#

command : poetry run uvicorn main:app

# docs

# to run so you can connect to front end with physical device

if you need ngrok:
npm install -g ngrok
signup
command : poetry run ngrok http 8000

if you are connected locally please visit
http://127.0.0.1:8000/docs

# mailhog (to see emails sent out for password reset)
-brew install mailhog (mac)
-in terminal, run: mailhog