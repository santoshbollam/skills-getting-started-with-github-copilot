"""Shared pytest fixtures and configuration for the test suite."""

import pytest
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI application."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Reset activities to their initial state before each test.
    This fixture ensures tests don't interfere with each other.
    """
    # Store original activities state
    initial_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Team-based basketball practice and friendly competitions",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": []
        },
        "Tennis Team": {
            "description": "Learn tennis skills and compete in matches",
            "schedule": "Tuesdays and Saturdays, 3:00 PM - 4:30 PM",
            "max_participants": 10,
            "participants": []
        },
        "Music Band": {
            "description": "Join our school band and perform at events",
            "schedule": "Wednesdays, 4:00 PM - 5:00 PM",
            "max_participants": 25,
            "participants": []
        },
        "Drawing Club": {
            "description": "Explore various drawing and painting techniques",
            "schedule": "Thursdays, 3:30 PM - 4:45 PM",
            "max_participants": 18,
            "participants": []
        },
        "Debate Club": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Mondays and Wednesdays, 3:45 PM - 4:45 PM",
            "max_participants": 16,
            "participants": []
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific discoveries",
            "schedule": "Tuesdays, 4:00 PM - 5:00 PM",
            "max_participants": 20,
            "participants": []
        }
    }

    # Clear and reset the activities dictionary
    activities.clear()
    activities.update(initial_activities)
    
    yield
    
    # Clean up after test
    activities.clear()
    activities.update(initial_activities)
