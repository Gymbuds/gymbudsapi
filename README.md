# gymbudsapi

Backend API for GymBuds

# poetry

-set up your poetry using: poetry install
-if you need to install new packages do: poetry add [package name]
-if you make changes to models: poetry run alembic revision --autogenerate -m

# set up your postgres DB

command : poetry run uvicorn main:app

# docs

if you are connected locally please visit
http://127.0.0.1:8000/docs

# mailhog (to see emails sent out for password reset)
-brew install mailhog
-in terminal, run: mailhog