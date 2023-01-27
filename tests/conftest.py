import pytest

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel

from app.main import app
from app.db import test_engine, get_session, get_test_session


app.dependency_overrides[get_session] = get_test_session


@pytest.fixture(scope="session")
def test_db():
    with Session(test_engine) as session:
        SQLModel.metadata.create_all(test_engine)
        yield session
        SQLModel.metadata.drop_all(test_engine)
    

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        SQLModel.metadata.create_all(test_engine)
        yield client
        SQLModel.metadata.drop_all(test_engine)
