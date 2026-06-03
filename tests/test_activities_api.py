from src.app import activities


def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Chess Club" in response.json()


def test_signup_for_activity_adds_participant(client):
    activity_name = "Chess Club"
    new_email = "student@example.com"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"
    assert new_email in activities[activity_name]["participants"]


def test_signup_duplicate_participant_returns_400(client):
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_remove_nonexistent_participant_returns_404(client):
    activity_name = "Chess Club"
    email = "notfound@example.com"

    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_signup_unknown_activity_returns_404(client):
    response = client.post(
        "/activities/Unknown/signup",
        params={"email": "student@example.com"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
