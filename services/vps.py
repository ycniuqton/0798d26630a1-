import requests


class VPSService:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }

    def create(self, payload):
        url = f"{self.base_url}/system/vpss/create"
        response = requests.post(url, headers=self.headers, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            # Handle errors as needed
            response.raise_for_status()


# Example usage
if __name__ == "__main__":
    base_url = "http://127.0.0.1:5000"
    api_key = "scrypt:32768:8:1$RL6X6J7bJJiROtTL$5bd54c34882906e9cf41e596c0a2b67f2a256b1492e266642f3c40521e4b4521ff56dfcf84e9deb9e34ea63d6e89de3c089d32041b5269d76f4c11078636aebd"

    service = VPSService(base_url, api_key)
    payload = {
        "hostname": "somehost",
        "password": "somepass",
        "serid": 0,
        "plid": 58,
        "osid": 100006
    }

    try:
        response = service.create(payload)
        print(response)
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")
