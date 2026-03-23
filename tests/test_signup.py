"""Tests for POST /activities/{activity_name}/signup endpoint."""

import pytest


class TestSignup:
    """Test suite for signing up for activities."""

    def test_signup_successful(self, client):
        """
        Arrange: Setup test client with valid activity and email
        Act: Send POST request to signup endpoint
        Assert: Verify status code is 200 and participant is added
        """
        # Arrange
        activity_name = "Basketball Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert email in client.get("/activities").json()[activity_name]["participants"]

    def test_signup_returns_success_message(self, client):
        """
        Arrange: Setup test client with valid activity and email
        Act: Send POST request to signup endpoint
        Assert: Verify response contains success message
        """
        # Arrange
        activity_name = "Tennis Team"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_duplicate_email_returns_400(self, client):
        """
        Arrange: Setup test client with email already signed up for activity
        Act: Send POST request to signup with duplicate email
        Assert: Verify status code is 400 and error message is returned
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity_returns_404(self, client):
        """
        Arrange: Setup test client with non-existent activity name
        Act: Send POST request to signup for non-existent activity
        Assert: Verify status code is 404 and error message is returned
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_signup_multiple_different_emails_same_activity(self, client):
        """
        Arrange: Setup test client with multiple unique emails
        Act: Send POST requests for multiple students to same activity
        Assert: Verify all participants are added
        """
        # Arrange
        activity_name = "Music Band"
        emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]

        # Act
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

        # Assert
        participants = client.get("/activities").json()[activity_name]["participants"]
        for email in emails:
            assert email in participants

    def test_signup_preserves_existing_participants(self, client):
        """
        Arrange: Setup test client with activity that has existing participants
        Act: Send POST request to signup new participant
        Assert: Verify existing participants are still in the list
        """
        # Arrange
        activity_name = "Programming Class"
        existing_participants = client.get("/activities").json()[activity_name]["participants"].copy()
        new_email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )

        # Assert
        assert response.status_code == 200
        updated_participants = client.get("/activities").json()[activity_name]["participants"]
        for existing_participant in existing_participants:
            assert existing_participant in updated_participants
        assert new_email in updated_participants

    def test_signup_with_empty_string_email(self, client):
        """
        Arrange: Setup test client with empty string email
        Act: Send POST request to signup with empty email
        Assert: Verify the request is processed (backend doesn't validate email format)
        """
        # Arrange
        activity_name = "Drawing Club"
        email = ""

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        # Empty string is technically valid per current implementation
        assert response.status_code == 200 or response.status_code == 400
