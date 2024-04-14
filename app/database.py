# importing statements
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Vaibhav.010402@localhost/fastapi"

# Creating the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session to talk to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# The function to set up the session for sql to be executed and db connection to be closed
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# All models extend this base class
Base = declarative_base()