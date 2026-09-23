from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_and_unregister_participant():
    activity_name = "Basketball Club"
    email = "newstudent@mergington.edu"

    # Ensure a clean state
    client.delete(f"/activities/{activity_name}/participants/{email}")

    sign_up_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert sign_up_response.status_code == 200

    activity_response = client.get("/activities")
    assert email in activity_response.json()[activity_name]["participants"]

    remove_response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert remove_response.status_code == 200
    assert "message" in remove_response.json()

    updated_response = client.get("/activities")
    assert email not in updated_response.json()[activity_name]["participants"]


def test_duplicate_signup_is_rejected():
    activity_name = "Basketball Club"
    email = "duplicate@mergington.edu"

    client.delete(f"/activities/{activity_name}/participants/{email}")

    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert first_response.status_code == 200

    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert second_response.status_code == 400
    assert "already signed up" in second_response.json()["detail"].lower()


def test_signup_for_unknown_activity_is_rejected():
    response = client.post("/activities/Unknown Club/signup?email=student@mergington.edu")

    assert response.status_code == 404
    assert "activity not found" in response.json()["detail"].lower()


def test_unregister_unknown_participant_is_rejected():
    activity_name = "Basketball Club"
    email = "missing@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 404
    assert "participant not found" in response.json()["detail"].lower()
