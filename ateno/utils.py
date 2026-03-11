import requests

class AtenoClient:
    def __init__(self, api_key=None, secret_key=None, base_url="https://us-central1-oyola-ai.cloudfunctions.net/api"):
        if not api_key and not secret_key:
            raise ValueError("[AtenoSDK] Initialization failed: You must provide either an api_key or a secret_key.")
        
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.request_count = 0

    def post(self, endpoint, payload):
        self.request_count += 1
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}

        if self.secret_key:
            headers["Authorization"] = f"Bearer {self.secret_key}"
        elif self.api_key:
            headers["x-api-key"] = self.api_key

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code in (401, 403):
            raise PermissionError("[AtenoSDK Auth Error] Invalid or inactive API key.")
        if response.status_code == 402:
            raise Exception("[AtenoSDK Billing Error] Insufficient credits.")
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            time_msg = f"in {retry_after}s" if retry_after else "later"
            raise Exception(f"[AtenoSDK Quota Error] Rate limit reached. Try again {time_msg}.")

        try:
            data = response.json()
        except ValueError:
            data = {}

        if not response.ok or data.get("status") == "error" or data.get("success") is False:
            error_msg = data.get("error") or data.get("message") or f"HTTP Error {response.status_code}"
            raise Exception(f"[AtenoSDK Error] {error_msg}")

        return data

    def get_total_requests(self):
        return self.request_count