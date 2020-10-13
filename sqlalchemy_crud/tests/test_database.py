"""
test_database

Hold config and fixtures for testing Database.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import pytest

DB_TYPE = "mysql+pymysql"
DB_HOST = "localhost"
DB_USER = os.environ["MYSQL_USER"]
DB_PASS = os.environ["MYSQL_PASSWORD"]
DB_NAME = os.environ["MYSQL_DATABASE"]

SQLALCHEMY_DATABASE_URL = f"{DB_TYPE}://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@pytest.fixture()
def setup_database():
    """ Fixture to setup and tear down a database for testing """

    Base.metadata.create_all(bind=engine)
    db: Session = session_local()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
