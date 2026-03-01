import requests

from .api_clients.health_client import HealthClient
from .api_clients.rsvps_client import RSVPSClient
from .conftest import BASE_URL, generate_user_data
from .api_clients.auth_client import AuthClient
from .api_clients.events_client import EventsClient
from .api_clients.health_client import HealthClient



### HAPPY PATH TESTS ###

def test_health_check():
    """check that health endpoint returns 'healthy'
    Make sure app is running to test this"""


    # Act
    response = HealthClient(BASE_URL).check_api_status()
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data['status'] == 'healthy'



def test_register_user_creates_new_user():
    """check that the registration of a new user works"""

    # Arrange
    auth = AuthClient(BASE_URL)
    user_data = generate_user_data()

    # Act: register user
    response = auth.register(user_data)

    # Assert
    assert response.status_code == 201
    assert response.json()['message'] == 'User created successfully'
    assert response.json()['user']['username'] == user_data['username']



def test_login_user_returns_auth_token():
    """check that we can login a registered user and get an auth token"""

    # Arrange
    user_data = generate_user_data()

    AuthClient(BASE_URL).register(user_data)

    # Act: login
    response = AuthClient(BASE_URL).login(user_data)

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
    event_creation_response = EventsClient(BASE_URL).create_event(event_data, headers)

    # Assert
    assert event_creation_response.status_code == 201



def test_rsvp_to_public_event_requires_no_auth(register_user_and_get_auth_token):
    """check that we can rsvp to a public event without auth"""

    # Arrange: register user
    auth_token = register_user_and_get_auth_token

    event_data = {
        "title": "Public Test Meetup",
        "description": "anybody should be able to join this",
        "date": "2030-11-15T18:00:00",
        "location": "at yo momma's",
        "capacity": 10,
        "is_public": True,
        "requires_admin": False
    }
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Arrange: create public event & get ID
    event_creation_response = EventsClient(BASE_URL).create_event(event_data, headers)
    event_id = event_creation_response.json()["id"]

    # Act: RSVP to event without auth
    reply = {"attending": True}
    rsvps_response = RSVPSClient(BASE_URL).rsvp_to_event(event_id, reply)

    # Assert RSVP was successful
    assert rsvps_response.status_code == 201



### ERROR/ EDGE CASE TESTS ###

def test_register_duplicate_user_fails():
    """check that registering a duplicate user returns 400"""

    # Arrange
    user_data = generate_user_data()

    # Act: register same user twice
    AuthClient(BASE_URL).register(user_data)
    duplicate_registration_response = AuthClient(BASE_URL).register(user_data)

    # Assert
    assert duplicate_registration_response.status_code == 400
    assert duplicate_registration_response.json()['error'] == 'Username already exists'



def test_rsvp_to_private_event_fails_without_auth_passes_with_auth(register_user_and_get_auth_token):
    """check that rsvp to private event without auth returns 401 error, bit rsvp to same event with auth passes"""

    # Arrange: register user
    auth_token = register_user_and_get_auth_token

    event_data = {
        "title": "Private Test Meetup",
        "description": "rsvp only possible with auth",
        "date": "2030-11-15T18:00:00",
        "location": "at yo momma's",
        "capacity": 5,
        "is_public": False,
        "requires_admin": False
    }
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Arrange: create public event & get ID
    event_creation_response = EventsClient(BASE_URL).create_event(event_data, headers)
    event_id = event_creation_response.json()["id"]

    # Act: RSVP to event without auth
    reply = {"attending": True}
    response_no_auth = RSVPSClient(BASE_URL).rsvp_to_event(event_id, reply)

    # Assert second RSVP fails due to missing auth
    assert response_no_auth.status_code == 401
    assert response_no_auth.json()['error'] == 'Authentication required for this event'


    # Act: RSVP to the same event again, this time with auth
    reply = {"attending": True}
    response_auth = RSVPSClient(BASE_URL).rsvp_to_event(event_id, reply, headers)

    assert response_auth.status_code == 201


def test_rsvp_to_admin_event_fails_with_non_admin_auth(register_user_and_get_auth_token):
    """check that rsvp to private event with non-admin token returns 403 error"""

    # Arrange: register user and get token for event creation
    auth_token = register_user_and_get_auth_token

    event_data = {
        "title": "Admin Test Meetup",
        "description": "rsvp only possible with admin-auth",
        "date": "2030-11-15T18:00:00",
        "location": "at yo momma's",
        "capacity": 5,
        "is_public": False,
        "requires_admin": True
    }
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Arrange: create admin event & get ID
    event_creation_response = EventsClient(BASE_URL).create_event(event_data, headers)
    event_id = event_creation_response.json()["id"]

    # Act: RSVP to event with non-admin auth
    reply = {"attending": True}
    response_auth = RSVPSClient(BASE_URL).rsvp_to_event(event_id, reply, headers)

    assert response_auth.status_code == 403
    assert response_auth.json()['error'] == 'Admin access required for this event'



def test_rsvp_to_booked_out_public_event_fails(register_user_and_get_auth_token):
    """check that rsvp to booked out public event returns 400 error"""

    # Arrange: register user
    auth_token = register_user_and_get_auth_token

    event_data = {
        "title": "Public Test Meetup; capacity is 1",
        "description": "has a capacity of 1",
        "date": "2030-11-15T18:00:00",
        "location": "at yo momma's",
        "capacity": 1,
        "is_public": True,
        "requires_admin": False
    }
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Arrange: create public event & get ID
    event_creation_response = EventsClient(BASE_URL).create_event(event_data, headers)
    event_id = event_creation_response.json()["id"]

    # Act: RSVP twice to event without auth
    reply = {"attending": True}
    response_first_rsvp = RSVPSClient(BASE_URL).rsvp_to_event(event_id, reply)

    #assert first rsvp was successful
    assert response_first_rsvp.status_code == 201

    #Act: RSVP to the same event again
    response_full_capacity = RSVPSClient(BASE_URL).rsvp_to_event(event_id, reply)

    # Assert second RSVP fails due to capacity being reached
    assert response_full_capacity.status_code == 400
    assert response_full_capacity.json()['error'] == 'Event is at full capacity'

