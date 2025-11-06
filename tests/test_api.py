from fastapi.testclient import TestClient
import pytest

from src.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect known activity keys from in-memory data
    assert "Chess Club" in data


def test_signup_and_unregister_flow(client):
    activity = "Chess Club"
    email = "test_student@example.com"

    # Ensure email not already in participants
    resp = client.get("/activities")
    assert resp.status_code == 200
    participants = resp.json()[activity]["participants"]
    if email in participants:
        participants.remove(email)

    # Signup
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert "Signed up" in signup_resp.json().get("message", "")

    # Verify participant present
    resp2 = client.get("/activities")
    assert resp2.status_code == 200
    participants_after = [p.lower() for p in resp2.json()[activity]["participants"]]
    assert email.lower() in participants_after

    # Attempt duplicate signup -> 400
    dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert dup.status_code == 400

    # Unregister
    unregister_resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert unregister_resp.status_code == 200
    assert "Unregistered" in unregister_resp.json().get("message", "")

    # Verify removed
    resp3 = client.get("/activities")
    participants_final = [p.lower() for p in resp3.json()[activity]["participants"]]
    assert email.lower() not in participants_final


def test_signup_nonexistent_activity(client):
    resp = client.post("/activities/Nonexistent%20Activity/signup?email=a@b.com")
    assert resp.status_code == 404
