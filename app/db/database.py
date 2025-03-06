from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from databases import Database
import os
from dotenv import load_dotenv
# Set the database URL, which should be PostgreSQL running on localhost
load_dotenv()
DATABASE_URL = os.getenv("DB_URL",f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
engine = create_engine(DATABASE_URL) 
metadata = MetaData()
Base = declarative_base(metadata=metadata)
database = Database(DATABASE_URL)

