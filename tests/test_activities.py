"""Tests for GET /activities endpoint."""

import pytest


class TestGetActivities:
    """Test suite for retrieving all activities."""

    def test_get_activities_returns_200(self, client):
        """
        Arrange: Setup test client
        Act: Send GET request to /activities
        Assert: Verify status code is 200
        """
        # Arrange
        expected_status = 200

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == expected_status

    def test_get_activities_returns_dict(self, client):
        """
        Arrange: Setup test client
        Act: Send GET request to /activities
        Assert: Verify response is a dictionary
        """
        # Arrange & Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert isinstance(data, dict)

    def test_get_activities_contains_all_activities(self, client):
        """
        Arrange: Define expected activity names
        Act: Send GET request to /activities
        Assert: Verify all activities are present
        """
        # Arrange
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class",
            "Basketball Club", "Tennis Team", "Music Band",
            "Drawing Club", "Debate Club", "Science Club"
        ]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert len(data) == len(expected_activities)
        for activity_name in expected_activities:
            assert activity_name in data

    def test_get_activities_response_structure(self, client):
        """
        Arrange: Setup test client
        Act: Send GET request to /activities
        Assert: Verify each activity has required fields
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            for field in required_fields:
                assert field in activity_data, f"Activity '{activity_name}' missing field '{field}'"
                assert activity_data[field] is not None, f"Activity '{activity_name}' field '{field}' is None"

    def test_get_activities_participants_field_is_list(self, client):
        """
        Arrange: Setup test client
        Act: Send GET request to /activities
        Assert: Verify participants field is a list for all activities
        """
        # Arrange & Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list), \
                f"Activity '{activity_name}' participants should be a list"

    def test_get_activities_with_existing_participants(self, client):
        """
        Arrange: Setup test client
        Act: Send GET request to /activities
        Assert: Verify activities with participants show correct list
        """
        # Arrange
        expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert data["Chess Club"]["participants"] == expected_chess_participants

    def test_get_activities_with_empty_participants(self, client):
        """
        Arrange: Setup test client
        Act: Send GET request to /activities
        Assert: Verify activities with no participants show empty list
        """
        # Arrange & Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert data["Basketball Club"]["participants"] == []
        assert data["Tennis Team"]["participants"] == []
