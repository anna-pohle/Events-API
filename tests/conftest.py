import pytest
import time

import requests

BASE_URL = "http://localhost:5000"

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def register_user_and_get_auth_token():
    """fixture that registers a user and returns an auth token"""

    # create unique username using timestamp
    timestamp= int(time.time()*1000)
    username = f"testuser{timestamp}"

    # register user
    user_data = {"username": username,
                 "password": "secret123!"}

    requests.post(f"{BASE_URL}/api/auth/register", json=user_data)

    # login
    response = requests.post(f"{BASE_URL}/api/auth/login", json=user_data)
    return response.json()["access_token"]