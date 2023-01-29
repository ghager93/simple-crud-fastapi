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


def _pop_datetimes(payload):
    """
    Removes datetimes from return values so as to compare to sample payloads in asserts. 
    Another possible option is to monkeypatch the datetime.now() function to return a 
    consistent result and have separate sample returns to test against.
    """
    if type(payload) == dict:
        payload.pop("created_at", "")
        payload.pop("updated_at", "")
    if type(payload) == list:
        for p in payload:
            p.pop("created_at", "")
            p.pop("updated_at", "")
    return payload


def test_hello_world(test_client: TestClient):
    """Test hello world endpoint returns correctly"""
    result = test_client.get("api/helloworld")

    assert result.status_code == 200
    assert result.json() == ["hello world!"]


def test_post_returns_2xx(test_client: TestClient):
    result = test_client.post("api/simple", json=valid_payload)

    assert 200 <= result.status_code < 300


def test_post_saved_to_db(test_client: TestClient, test_db: Session):
    from app.models import Simple

    test_client.post("api/simple", json=valid_payload)

    result = test_db.query(Simple).filter(Simple.name == valid_payload["name"]).first()

    assert result.name == valid_payload["name"]
    assert result.number == valid_payload["number"]


def test_post_invalid_4xx_status(test_client: TestClient):
    """Test invalid post returns correct code."""
    result = test_client.post("api/simple", json=invalid_payload)

    assert 400 <= result.status_code < 500


def test_post_invalid_not_saved_to_db(test_client: TestClient, test_db: Session):
    """Test invalid entry is not saved to db."""
    from app.models import Simple

    test_client.post("api/simple", json=invalid_payload)
    result = test_db.query(Simple).all()

    assert result == []


def test_get_all_2xx_status(test_client: TestClient):
    result = test_client.get("api/simple")

    assert 200 <= result.status_code < 300


def test_get_all_empty_return(test_client: TestClient):
    result = test_client.get("api/simple")

    assert result.json() == []


def test_get_all_one_return(test_client: TestClient):
    test_client.post("api/simple", json=valid_payload)
    
    result = test_client.get("api/simple")

    assert _pop_datetimes(result.json()) == [valid_payload]


def test_get_all_three_return(test_client: TestClient):
    [test_client.post("api/simple", json=valid_payloads[i]) for i in range(3)]

    result = test_client.get("api/simple")

    assert sorted(_pop_datetimes(result.json()), key=lambda x: x["name"]) == sorted(
        valid_payloads, key=lambda x: x["name"]
    )


def test_get_valid_id_2xx_status(test_client: TestClient):
    test_client.post("api/simple", json=valid_payload)

    result = test_client.get("api/simple/1")

    assert 200 <= result.status_code < 300 


def test_get_invalid_id_404_status(test_client: TestClient):
    test_client.post("api/simple", json=valid_payload)

    result = test_client.get("api/simple/2")

    assert result.status_code == 404


def test_get_valid_id(test_client: TestClient):
    test_client.post("api/simple", json=valid_payload)

    result = test_client.get("api/simple/1")

    assert _pop_datetimes(result.json()) == valid_payload


def test_delete_valid_id_2xx_status(test_client: TestClient):
    test_client.post("api/simple", json=valid_payload)

    result = test_client.delete("api/simple/1")

    assert 200 <= result.status_code < 300


def test_delete_invalid_id_404_status(test_client: TestClient):
    test_client.post("api/simple", json=valid_payload)

    result = test_client.delete("api/simple/2")

    assert result.status_code == 404


def test_delete_valid_id(test_client: TestClient):
    test_client.post("api/simple", json=valid_payload)

    first_result = test_client.delete("api/simple/1")
    second_result = test_client.delete("api/simple/1")

    assert _pop_datetimes(first_result.json()) == valid_payload
    assert second_result.status_code == 404
    

def test_patch_valid_id_2xx_status(test_client: TestClient):
    test_client.post("api/simple", json=valid_payload)

    result = test_client.patch("api/simple/1", json=patched_name_payload)

    assert 200 <= result.status_code < 300


def test_patch_invalid_id_404_status(test_client: TestClient):
    test_client.post("api/simple", json=valid_payload)

    result = test_client.patch("api/simple/2", json=patched_name_payload)

    assert result.status_code == 404


def test_patch_valid_id_patch_name(test_client: TestClient):
    test_client.post("api/simple", json=valid_payload)

    result_patch = test_client.patch("api/simple/1", json=patched_name_payload)
    result_get = test_client.get("api/simple/1")

    assert result_patch.json()["name"] == patched_name_payload["name"]
    assert result_patch.json()["number"] == valid_payload["number"]
    assert result_get.json()["name"] == patched_name_payload["name"]
    assert result_get.json()["number"] == valid_payload["number"]


def test_patch_valid_id_patch_number(test_client: TestClient):
    test_client.post("api/simple", json=valid_payload)

    result_patch = test_client.patch("api/simple/1", json=patched_number_payload)
    result_get = test_client.get("api/simple/1")

    assert result_patch.json()["name"] == valid_payload["name"]
    assert result_patch.json()["number"] == patched_number_payload["number"]
    assert result_get.json()["name"] == valid_payload["name"]
    assert result_get.json()["number"] == patched_number_payload["number"]