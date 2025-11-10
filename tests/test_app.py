from fastapi.testclient import TestClient
import pytest

from src.app import app, activities


@pytest.fixture
def client():
    return TestClient(app)


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # should be a mapping with at least one activity
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow(client):
    activity = "Chess Club"
    test_email = "pytest-test@example.com"

    # Ensure test email is not present
    if test_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(test_email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert resp.status_code == 200
    assert resp.json()["message"].startswith("Signed up")
    assert test_email in activities[activity]["participants"]

    # Sign up duplicate should fail
    resp_dup = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert resp_dup.status_code == 400

    # Unregister
    resp_unreg = client.delete(f"/activities/{activity}/unregister", params={"email": test_email})
    assert resp_unreg.status_code == 200
    assert resp_unreg.json()["message"].startswith("Unregistered")
    assert test_email not in activities[activity]["participants"]
