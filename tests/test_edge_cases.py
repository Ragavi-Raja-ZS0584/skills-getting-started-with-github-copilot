"""Tests for edge cases and additional validation."""
import pytest


def test_email_case_sensitivity(client):
    """Test if emails are case-sensitive."""
    activity_name = "Chess Club"
    email_lower = "student@test.edu"
    email_upper = "STUDENT@TEST.EDU"

    # Signup with lowercase
    response = client.post(f"/activities/{activity_name}/signup?email={email_lower}")
    assert response.status_code == 200

    # Try to signup with uppercase - should be treated as different email
    response = client.post(f"/activities/{activity_name}/signup?email={email_upper}")
    # Based on current implementation, emails are case-sensitive
    # If this succeeds, emails are case-sensitive
    # If it fails with 400, they are case-insensitive
    # From app.py, it uses list membership which is case-sensitive in Python
    assert response.status_code == 200  # Should succeed as different email


def test_activity_name_with_spaces(client):
    """Test activity names with spaces."""
    activity_name = "Chess Club"  # Has space
    email = "student@test.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    # Verify in activities list
    response = client.get("/activities")
    activities = response.json()
    assert activity_name in activities
    assert email in activities[activity_name]["participants"]


def test_empty_email_signup(client):
    """Test signup with empty email."""
    activity_name = "Chess Club"
    email = ""

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Current implementation doesn't validate email format
    # It will accept empty string
    assert response.status_code == 200

    # Verify empty email was added
    response = client.get("/activities")
    activities = response.json()
    assert "" in activities[activity_name]["participants"]


def test_special_characters_in_activity_name(client):
    """Test activity names with special characters."""
    # Use an activity with special characters
    activity_name = "Drama & Theater"  # Has space and &
    email = "student@test.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200


def test_max_participants_not_enforced(client):
    """Test that max_participants is not currently enforced."""
    activity_name = "Chess Club"
    email1 = "student1@test.edu"
    email2 = "student2@test.edu"

    # Get max participants for Chess Club
    response = client.get("/activities")
    activities = response.json()
    max_participants = activities[activity_name]["max_participants"]

    # Signup more than max_participants
    for i in range(max_participants + 1):
        email = f"student{i}@test.edu"
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        # Current implementation doesn't check max_participants
        assert response.status_code == 200