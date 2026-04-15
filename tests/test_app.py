from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate_returns_bad_request():
    email = "michael@mergington.edu"
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant():
    email = "michael@mergington.edu"
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"
    assert email not in activities["Chess Club"]["participants"]


def test_remove_missing_participant_returns_not_found():
    email = "missing@mergington.edu"
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": email},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
