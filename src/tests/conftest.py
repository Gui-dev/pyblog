
import sys
import os
import pytest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.database.database import Base
from src.database.dependencies import get_db
from src.server import app


SQLALCHEMY_DATABASE_URL = "sqlite:///./src/tests/test.db"

engine = create_engine(
	SQLALCHEMY_DATABASE_URL,
	connect_args={ 'check_same_thread': False }
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
	try:
		db = TestingSessionLocal()
		yield db
	finally:
		db.close()
		

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope='session', autouse=True)
def setup_test_db():
	Base.metadata.create_all(bind=engine)
	yield
	Base.metadata.drop_all(bind=engine)
	
	
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client
        
