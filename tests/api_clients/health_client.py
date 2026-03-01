import requests


class HealthClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def check_api_status(self) -> requests.Response:
            return requests.get(f"{self.base_url}/api/health")

