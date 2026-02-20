import requests
from .conftest import BASE_URL
import time



### HAPPY PATH TESTS ###

def test_health_check():
    """check that health endpoint returns 'healthy'
    Make sure app is running to test this"""

    #Arrange

    # Act
    response = requests.get(f"{BASE_URL}/api/health")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data['status'] == 'healthy'



def test_register_user_creates_new_user():
    """check that the registration of a new user works"""

    # Arrange
    user_data = generate_user_data()

    # Act: register user
    response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)

    # Assert
    assert response.status_code == 201
    assert response.json()['message'] == 'User created successfully'
    assert response.json()['user']['username'] == user_data['username']



def test_login_user_returns_auth_token():
    """check that we can login a registered user and get an auth token"""

    # Arrange
    user_data = generate_user_data()

    requests.post(f"{BASE_URL}/api/auth/register", json=user_data)

    # Act: login
    response = requests.post(f"{BASE_URL}/api/auth/login", json=user_data)

    # Assert
    assert response.status_code == 200
    assert response.json()["user"]["username"] == user_data["username"]
    assert response.json()["access_token"] is not None
    assert response.json()["access_token"] is not ""


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

    # Arrange

    # Act

    # Assert
    pass



### ERROR/ EDGE CASE TESTS ###

def test_register_duplicate_user_fails(register_user_and_get_auth_token):
    """check that registering a duplicate user returns 400"""

    # Arrange

    # Act

    # Assert

    pass



def test_rsvp_to_private_event_fails_without_auth():
    """check that rsvp to private event without auth returns 401 error"""

    # Arrange

    # Act

    # Assert

    pass



def test_rsvp_to_private_event_fails_with_invalid_token():
    """check that rsvp to private event with invalid token returns 401 error"""

    # Arrange

    # Act

    # Assert

    pass



def test_rsvp_to_booked_out_event_fails():
    """check that rsvp to booked out event returns 400 error"""

    # Arrange

    # Act

    # Assert

    pass



### HELPER FUNCTIONS ###

def generate_user_data():
    # create unique username using timestamp
    timestamp = int(time.time() * 1000)
    username = f"testuser{timestamp}"

    # register user
    user_data = {"username": username,
                 "password": "secret123!"}
    return user_data