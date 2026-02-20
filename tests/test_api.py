import datetime

import requests
from .conftest import BASE_URL

### HAPPY PATH TESTS ###

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

def test_register_user_creates_new_user():
    """check that we can register a user"""
    pass


def test_login_user_returns_auth_token():
    """check that we can login a user and get an auth token"""
    pass

def test_create_public_event_requires_auth_and_suceeds_with_token(register_user_and_get_auth_token):
    """check that we can create a public event using an auth token"""

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
    headers = {"Authorization": f"Bearer {register_user_and_get_auth_token}"}

    # Act
    response = requests.post(f"{BASE_URL}/api/events",                             json=event_data,
                             headers=headers)

    # Assert
    assert response.status_code == 201

def test_rsvp_to_public_event_requires_no_auth(register_user_and_get_auth_token):
    """check that we can rsvp to a public event without auth"""
    pass


### ERROR/ EDGE CASE TESTS ###

def test_register_duplicate_user_fails():
    """check that registering a duplicate user returns 400"""
    pass

def test_rsvp_to_private_event_fails_without_auth():
    """check that rsvp to private event without auth returns 401 error"""
    pass

def test_rsvp_to_private_event_fails_with_invalid_token():
    """check that rsvp to private event with invalid token returns 401 error"""
    pass

def test_rsvp_to_booked_out_event_fails():
    """check that rsvp to booked out event returns 400 error"""