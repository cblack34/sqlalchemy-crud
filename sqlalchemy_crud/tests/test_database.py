import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pytest

db_type = "mysql+pymysql"
db_host = "localhost"
db_user = os.environ["MYSQL_USER"]
db_pass = os.environ["MYSQL_PASSWORD"]
db_name = os.environ["MYSQL_DATABASE"]

SQLALCHEMY_DATABASE_URL = f"{db_type}://{db_user}:{db_pass}@{db_host}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@pytest.fixture()
def setup_database():
    """ Fixture to setup and tear down a database for testing """

    Base.metadata.create_all(bind=engine)
    db = session_local()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
