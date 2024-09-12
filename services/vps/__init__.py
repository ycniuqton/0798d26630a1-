from tenacity import retry, stop_after_attempt, wait_fixed
import requests

from home.models import Vps, VpsStatus


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

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def stop(self, vps_id):
        url = f"{self.base_url}/system/vpss/{vps_id}/stop"
        response = requests.post(url, headers=self.headers)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            # Raise an HTTP error for non-200 status codes
            response.raise_for_status()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def restart(self, vps_id):
        url = f"{self.base_url}/system/vpss/{vps_id}/restart"
        response = requests.post(url, headers=self.headers)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            # Raise an HTTP error for non-200 status codes
            response.raise_for_status()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def start(self, vps_id):
        url = f"{self.base_url}/system/vpss/{vps_id}/start"
        response = requests.post(url, headers=self.headers)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            # Raise an HTTP error for non-200 status codes
            response.raise_for_status()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def suspend(self, vps_id):
        url = f"{self.base_url}/system/vpss/{vps_id}/suspend"
        response = requests.post(url, headers=self.headers)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            # Raise an HTTP error for non-200 status codes
            response.raise_for_status()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def unsuspend(self, vps_id):
        url = f"{self.base_url}/system/vpss/{vps_id}/unsuspend"
        response = requests.post(url, headers=self.headers)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            # Raise an HTTP error for non-200 status codes
            response.raise_for_status()

    @staticmethod
    def error(vps_id, message):
        vps = Vps.objects.get(id=vps_id)
        if not vps:
            return False
        vps.status = VpsStatus.ERROR
        vps.error_message = message
        vps.save()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def rebuild(self, payload):
        vps_id = payload.get('vps_id')
        url = f"{self.base_url}/system/vpss/{vps_id}/rebuild"
        response = requests.post(url, headers=self.headers, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            try:
                if response.json().get('success'):
                    return True
                else:
                    return False
            except Exception as e:
                raise e
        else:
            # Raise an HTTP error for non-200 status codes
            response.raise_for_status()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def get_stat(self, vps_ids):
        url = f"{self.base_url}/system/vpss/stat"
        if not vps_ids:
            response = requests.post(url, headers=self.headers)
        else:
            response = requests.post(url, headers=self.headers, json={'vps_ids': vps_ids})

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            # Raise an HTTP error for non-200 status codes
            response.raise_for_status()


class CtvVPSService(VPSService):
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def create(self, payload):
        url = f"{self.base_url}/api/vps/create"
        response = requests.post(url, headers=self.headers, json=payload.get('raw_data'))

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception({
                "code": response.status_code,
                "message": response.text
            })

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def stop(self, vps_id):
        url = f"{self.base_url}/api/vps/stop/"
        response = requests.post(url, headers=self.headers, json={'linked_ids': [vps_id]})

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            # Raise an HTTP error for non-200 status codes
            response.raise_for_status()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def restart(self, vps_id):
        url = f"{self.base_url}/api/vps/restart/"
        response = requests.post(url, headers=self.headers, json={'linked_ids': [vps_id]})

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            # Raise an HTTP error for non-200 status codes
            response.raise_for_status()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def start(self, vps_id):
        url = f"{self.base_url}/api/vps/start/"
        response = requests.post(url, headers=self.headers, json={'linked_ids': [vps_id]})

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            # Raise an HTTP error for non-200 status codes
            response.raise_for_status()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def suspend(self, vps_id):
        url = f"{self.base_url}/api/vps/suspend/"
        response = requests.post(url, headers=self.headers, json={'linked_ids': [vps_id]})

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            # Raise an HTTP error for non-200 status codes
            response.raise_for_status()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def unsuspend(self, vps_id):
        url = f"{self.base_url}/api/vps/unsuspend/"
        response = requests.post(url, headers=self.headers, json={'linked_ids': [vps_id]})

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            # Raise an HTTP error for non-200 status codes
            response.raise_for_status()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def rebuild(self, payload):
        vps_id = payload.get('vps_id')
        url = f"{self.base_url}/api/vps/rebuild/"
        raw_data = payload.get('raw_data')
        raw_data['linked_id'] = vps_id
        raw_data.pop('vps_id', None)
        response = requests.post(url, headers=self.headers, json=payload.get('raw_data'))

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            # Raise an HTTP error for non-200 status codes
            response.raise_for_status()
