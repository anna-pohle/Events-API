import datetime

import requests
from .conftest import BASE_URL

def test_health_check():
    """check that health endpoint returns healthy
    Make sure app is running to test this"""

    #Arrange

    # Act
    response = requests.get(f"{BASE_URL}/api/health")
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert data['status'] == 'healthy'

def test_create_event(auth_token):
    """check that we can create an event"""

    # Arrange event data
    event_data = {
      "title": "Test Meetup",
      "description": "blah",
      "date": "2026-11-15T18:00:00",
      "location": "at yo momma's",
      "capacity": 3,
      "is_public": True,
      "requires_admin": False
    }
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Act
    response = requests.post(f"{BASE_URL}/api/events",                             json=event_data,
                             headers=headers)

    # Assert
    assert response.status_code == 201
