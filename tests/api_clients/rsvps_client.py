import requests


class RSVPSClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def rsvp_to_event(self, event_id, reply, headers=None) -> requests.Response:
            return requests.post(f"{self.base_url}/api/rsvps/event/{event_id}", json=reply ,headers=headers)

