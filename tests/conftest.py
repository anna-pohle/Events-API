import pytest
import time
from tests.api_clients.auth_client import AuthClient

BASE_URL = "http://localhost:5000"



@pytest.fixture
def base_url():
    return BASE_URL



def generate_user_data() -> dict:
    # create unique username using timestamp
    timestamp = int(time.time() * 1000)
    username = f"testuser{timestamp}"

    # generate user_data as dict
    user_data = {"username": username,
                 "password": "secret123!"}
    return user_data



@pytest.fixture
def register_user_and_get_auth_token():
    """fixture that registers a user and returns an auth token"""

    # register user
    user_data = generate_user_data()
    AuthClient(BASE_URL).register(user_data)

    # login
    response = AuthClient(BASE_URL).login(user_data)
    return response.json()["access_token"]
