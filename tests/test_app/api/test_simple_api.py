from fastapi.testclient import TestClient


def test_hello_world(test_client: TestClient):
    """Test hello world endpoint returns correctly"""
    result = test_client.get("api/helloworld")

    assert result.status_code == 200
    assert result.json() == ["hello world!"]


def test_post_returns_2xx(test_client: TestClient):
    result = test_client.post("api/simple", json={})

    assert 200 <= result.status_code < 300

