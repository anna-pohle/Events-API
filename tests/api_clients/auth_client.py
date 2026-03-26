import requests


class AuthClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def register(self, user_data) -> requests.Response:
        return requests.post(f"{self.base_url}/api/auth/register", json=user_data)

    def login(self, user_data) -> requests.Response:
        return requests.post(f"{self.base_url}/api/auth/login", json=user_data)

