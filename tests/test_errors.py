"""Tests for error handling and edge cases."""

import pytest


class TestErrorHandling:
    """Test suite for error responses and edge cases."""

    def test_signup_error_response_format(self, client):
        """
        Arrange: Setup test client with duplicate signup
        Act: Send POST request that will fail
        Assert: Verify error response contains detail field
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
        data = response.json()
        assert "detail" in data
        assert isinstance(data["detail"], str)

    def test_unregister_error_response_format(self, client):
        """
        Arrange: Setup test client with unregister attempt
        Act: Send POST request to unregister non-existent participant
        Assert: Verify error response contains detail field
        """
        # Arrange
        activity_name = "Basketball Club"
        email = "notregistered@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert isinstance(data["detail"], str)

    def test_404_error_for_signup_invalid_activity(self, client):
        """
        Arrange: Setup test client with invalid activity
        Act: Send POST request to invalid activity
        Assert: Verify 404 response with detail message
        """
        # Arrange
        activity_name = "Fake Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_404_error_for_unregister_invalid_activity(self, client):
        """
        Arrange: Setup test client with invalid activity
        Act: Send POST request to invalid activity unregister
        Assert: Verify 404 response with detail message
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_signup_missing_email_parameter(self, client):
        """
        Arrange: Setup test client
        Act: Send POST request without email parameter
        Assert: Verify appropriate error response
        """
        # Arrange
        activity_name = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity_name}/signup")

        # Assert - Query parameter is required
        assert response.status_code in [400, 422]

    def test_unregister_missing_email_parameter(self, client):
        """
        Arrange: Setup test client
        Act: Send POST request without email parameter
        Assert: Verify appropriate error response
        """
        # Arrange
        activity_name = "Gym Class"

        # Act
        response = client.post(f"/activities/{activity_name}/unregister")

        # Assert - Query parameter is required
        assert response.status_code in [400, 422]

    def test_error_messages_include_email(self, client):
        """
        Arrange: Setup test client
        Act: Send POST request that will fail
        Assert: Verify error message includes email address
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        detail = response.json()["detail"]
        assert email in detail

    def test_error_messages_include_activity_name(self, client):
        """
        Arrange: Setup test client
        Act: Send POST request that will fail
        Assert: Verify error message includes activity name
        """
        # Arrange
        activity_name = "Programming Class"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # First signup succeeds
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert - Second attempt should fail with activity name in message
        assert response.status_code == 400
        detail = response.json()["detail"]
        assert activity_name in detail

    def test_success_response_includes_email(self, client):
        """
        Arrange: Setup test client
        Act: Send successful POST request to signup
        Assert: Verify success message includes email address
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
        message = response.json()["message"]
        assert email in message

    def test_success_response_includes_activity_name(self, client):
        """
        Arrange: Setup test client
        Act: Send successful POST request to signup
        Assert: Verify success message includes activity name
        """
        # Arrange
        activity_name = "Tennis Team"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        message = response.json()["message"]
        assert activity_name in message
