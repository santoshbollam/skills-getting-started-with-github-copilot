"""Tests for POST /activities/{activity_name}/unregister endpoint."""

import pytest


class TestUnregister:
    """Test suite for unregistering from activities."""

    def test_unregister_successful(self, client):
        """
        Arrange: Setup test client with participant in activity
        Act: Send POST request to unregister endpoint
        Assert: Verify status code is 200 and participant is removed
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert email not in client.get("/activities").json()[activity_name]["participants"]

    def test_unregister_returns_success_message(self, client):
        """
        Arrange: Setup test client with participant in activity
        Act: Send POST request to unregister endpoint
        Assert: Verify response contains success message
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_nonparticipant_returns_400(self, client):
        """
        Arrange: Setup test client with email not signed up for activity
        Act: Send POST request to unregister non-participant
        Assert: Verify status code is 400 and error message is returned
        """
        # Arrange
        activity_name = "Basketball Club"
        email = "notregistered@mergington.edu"  # Not signed up

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_nonexistent_activity_returns_404(self, client):
        """
        Arrange: Setup test client with non-existent activity name
        Act: Send POST request to unregister from non-existent activity
        Assert: Verify status code is 404 and error message is returned
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
        assert "not found" in response.json()["detail"]

    def test_unregister_preserves_other_participants(self, client):
        """
        Arrange: Setup test client with activity that has multiple participants
        Act: Send POST request to unregister one participant
        Assert: Verify other participants are still in the list
        """
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        email_to_preserve = "daniel@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email_to_remove}
        )

        # Assert
        assert response.status_code == 200
        participants = client.get("/activities").json()[activity_name]["participants"]
        assert email_to_remove not in participants
        assert email_to_preserve in participants

    def test_unregister_twice_returns_400(self, client):
        """
        Arrange: Setup test client, unregister a participant once
        Act: Attempt to unregister the same participant again
        Assert: Verify second unregister returns 400
        """
        # Arrange
        activity_name = "Programming Class"
        email = "sophia@mergington.edu"

        # Act - First unregister (should succeed)
        response1 = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Act - Second unregister (should fail)
        response2 = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 400
        assert "not signed up" in response2.json()["detail"]

    def test_unregister_allows_re_signup(self, client):
        """
        Arrange: Setup test client, unregister a participant
        Act: Sign up the same participant again
        Assert: Verify participant can re-signup after unregistering
        """
        # Arrange
        activity_name = "Gym Class"
        email = "john@mergington.edu"

        # Act - Unregister
        response1 = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Act - Re-signup
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert email in client.get("/activities").json()[activity_name]["participants"]

    def test_unregister_from_empty_activity(self, client):
        """
        Arrange: Setup test client, ensure activity has no participants
        Act: Send POST request to unregister from empty activity
        Assert: Verify status code is 400
        """
        # Arrange
        activity_name = "Basketball Club"  # Starts empty
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]
