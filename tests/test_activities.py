"""Tests for activities endpoints."""
import pytest


def test_get_activities(client):
    """Test getting all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()

    # Should return a dictionary with activity names as keys
    assert isinstance(data, dict)
    assert len(data) > 0  # Should have activities

    # Check structure of first activity
    first_activity = next(iter(data.values()))
    assert "description" in first_activity
    assert "schedule" in first_activity
    assert "max_participants" in first_activity
    assert "participants" in first_activity
    assert isinstance(first_activity["participants"], list)


def test_signup_success(client):
    """Test successful student signup."""
    activity_name = "Chess Club"
    email = "student@test.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert email in data["message"]

    # Verify the email was added to participants
    response = client.get("/activities")
    activities = response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate(client):
    """Test duplicate signup prevention."""
    activity_name = "Chess Club"
    email = "duplicate@test.edu"

    # First signup should succeed
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    # Second signup should fail
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_invalid_activity(client):
    """Test signup to non-existent activity."""
    activity_name = "NonExistent Activity"
    email = "student@test.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_success(client):
    """Test successful unregistration."""
    activity_name = "Chess Club"
    email = "unregister@test.edu"

    # First signup
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Then unregister
    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert email in data["message"]

    # Verify the email was removed from participants
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_not_registered(client):
    """Test unregistering non-participant."""
    activity_name = "Chess Club"
    email = "notregistered@test.edu"

    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"].lower()


def test_unregister_invalid_activity(client):
    """Test unregistering from non-existent activity."""
    activity_name = "NonExistent Activity"
    email = "student@test.edu"

    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()