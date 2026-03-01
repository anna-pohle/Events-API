import requests


class EventsClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_event(self, event_data, headers) -> requests.Response:
            return requests.post(f"{self.base_url}/api/events", json=event_data, headers=headers)

