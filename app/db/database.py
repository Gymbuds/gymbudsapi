from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from databases import Database
import os

# Set the database URL, which should be PostgreSQL running on localhost
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:12345@localhost/postgres")

# SQLAlchemy Setup
engine = create_engine(DATABASE_URL) 
metadata = MetaData()
Base = declarative_base(metadata=metadata)

database = Database(DATABASE_URL)
