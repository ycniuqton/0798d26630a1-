from tenacity import retry, stop_after_attempt, wait_fixed
import requests


class VPSService:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def create(self, payload):
        url = f"{self.base_url}/system/vpss/create"
        response = requests.post(url, headers=self.headers, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            # Raise an HTTP error for non-200 status codes
            response.raise_for_status()