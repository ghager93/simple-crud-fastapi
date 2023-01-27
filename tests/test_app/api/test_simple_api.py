from fastapi.testclient import TestClient
from sqlmodel import Session


valid_payload = {
    "name": "a name",
    "number": 1324,
}
invalid_payload = {"not string": "invalid"}

valid_payloads = [{"name": str(i), "number": i} for i in range(3)]

patched_name_payload = {
    "name": "patched name",
}

patched_number_payload = {
    "number": 5678,
}


def test_hello_world(test_client: TestClient):
    """Test hello world endpoint returns correctly"""
    result = test_client.get("api/helloworld")

    assert result.status_code == 200
    assert result.json() == ["hello world!"]


def test_post_returns_2xx(test_client: TestClient):
    result = test_client.post("api/simple", json={})

    assert 200 <= result.status_code < 300


def test_post_saved_to_db(test_client: TestClient, test_db: Session):
    from app.models import Simple
    test_client.post("api/simple", json=valid_payload)

    result = test_db.query(Simple).filter(Simple.name == valid_payload["name"]).first()

    assert result.name == valid_payload["name"]
    assert result.number == valid_payload["number"]

