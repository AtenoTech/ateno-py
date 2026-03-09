import requests

class AtenoClient:
    def __init__(self, api_key, base_url="https://api.ateno.ai"):
        self.api_key = api_key
        self.base_url = base_url

    def create_event(self, name, data):
        r = requests.post(
            f"{self.base_url}/events",
            json={"name": name, "data": data},
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return r.json()