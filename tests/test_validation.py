"""Tests for validation logic and edge cases."""

import pytest


class TestValidation:
    """Test suite for validation and edge cases."""

    def test_activity_name_case_sensitivity_in_signup(self, client):
        """
        Arrange: Setup test client with different case activity name
        Act: Send POST request with wrong case activity name
        Assert: Verify request fails with 404
        """
        # Arrange
        activity_name = "chess club"  # Wrong case
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404

    def test_activity_name_case_sensitivity_in_unregister(self, client):
        """
        Arrange: Setup test client with different case activity name
        Act: Send POST request with wrong case activity name
        Assert: Verify request fails with 404
        """
        # Arrange
        activity_name = "programming class"  # Wrong case
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404

    def test_max_participants_field_exists(self, client):
        """
        Arrange: Setup test client
        Act: Fetch activities and check max_participants field
        Assert: Verify max_participants is present and is an integer
        """
        # Arrange & Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            assert "max_participants" in activity_data
            assert isinstance(activity_data["max_participants"], int)
            assert activity_data["max_participants"] > 0

    def test_signup_does_not_enforce_capacity_limit(self, client):
        """
        Arrange: Setup test client with activity at capacity
        Act: Continue signing up participants beyond max_participants
        Assert: Verify current implementation allows over-capacity signup
        (This documents current behavior - not a feature)
        """
        # Arrange
        activity_name = "Tennis Team"  # max_participants = 10
        # Start with 0 participants, try to add 11

        # Act
        for i in range(11):
            email = f"student{i}@mergington.edu"
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )

        # Assert - Document that current implementation doesn't enforce capacity
        participants = client.get("/activities").json()[activity_name]["participants"]
        # Current implementation allows over-capacity
        assert len(participants) == 11

    def test_special_characters_in_activity_name(self, client):
        """
        Arrange: Setup test client with special characters in activity name
        Act: Send POST request with special characters
        Assert: Verify request returns 404 (activity not found)
        """
        # Arrange
        activity_name = "Chess Club!@#"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404

    def test_url_encoded_activity_name(self, client):
        """
        Arrange: Setup test client with URL-encoded activity name
        Act: Send POST request with properly encoded activity name
        Assert: Verify request succeeds
        """
        # Arrange
        activity_name = "Basketball Club"
        email = "student@mergington.edu"
        from urllib.parse import quote
        encoded_activity = quote(activity_name)

        # Act
        response = client.post(
            f"/activities/{encoded_activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200

    def test_email_with_special_characters(self, client):
        """
        Arrange: Setup test client with email containing special characters
        Act: Send POST request with special character email (valid format)
        Assert: Verify request succeeds (no email validation)
        """
        # Arrange
        activity_name = "Drawing Club"
        email = "student+test@mergington.edu"  # Valid email format with +

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200

    def test_very_long_email_address(self, client):
        """
        Arrange: Setup test client with very long email address
        Act: Send POST request with long email
        Assert: Verify request succeeds (no length validation)
        """
        # Arrange
        activity_name = "Science Club"
        email = "a" * 200 + "@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert - Current implementation doesn't validate email length
        assert response.status_code == 200

    def test_whitespace_only_email(self, client):
        """
        Arrange: Setup test client with whitespace-only email
        Act: Send POST request with whitespace email
        Assert: Verify request is processed (no validation)
        """
        # Arrange
        activity_name = "Debate Club"
        email = "   "

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200 or response.status_code == 400

    def test_duplicate_signup_preserves_single_entry(self, client):
        """
        Arrange: Setup test client, signup a participant successfully
        Act: Attempt duplicate signup
        Assert: Verify participant appears only once in the list
        """
        # Arrange
        activity_name = "Music Band"
        email = "newstudent@mergington.edu"

        # Act - First signup
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Act - Attempt duplicate
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 400
        
        participants = client.get("/activities").json()[activity_name]["participants"]
        count = participants.count(email)
        assert count == 1, f"Email appears {count} times, expected 1"
