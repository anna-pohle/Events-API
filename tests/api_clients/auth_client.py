import requests

from tests.conftest import generate_user_data


class AuthClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def register(self, user_data) -> requests.Response:
        return requests.post(f"{self.base_url}/api/auth/register", json=user_data)

    def login(self, user_data) -> requests.Response:
        return requests.post(f"{self.base_url}/api/auth/login", json=user_data)

    def login(self, username, password) -> requests.Response:
        return requests.post(f"{self.base_url}/api/auth/login", json={"username": username,
                 "password": password})

    def login(self) -> requests.Response:
        return requests.post(f"{self.base_url}/api/auth/login", json=generate_user_data())#TODO