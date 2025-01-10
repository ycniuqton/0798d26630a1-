from tenacity import retry, stop_after_attempt, wait_fixed
import requests

from adapters.redis_service.resources.full_data_server_group import CachedServerGroupConfig
from config import VIRTUALIZOR_CONFIG
from core import settings
from home.models import Vps, VpsStatus


class VPSService:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }

    # @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def create(self, payload):
        # group_configs = CachedServerGroupConfig().get()
        url = f"{self.base_url}/system/vpss/create"
        # is_locked = CachedServerGroupConfig().get_locked(payload.get('server_group'))
        # if is_locked:
        #     payload['serid'] = is_locked
        #     del payload['server_group']
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
    def delete(self, vps_id):
        url = f"{self.base_url}/system/vpss/{vps_id}/delete"
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
    def change_hostname(self, vps_id, payload):
        url = f"{self.base_url}/system/vpss/{vps_id}/change_hostname"
        response = requests.post(url, headers=self.headers, json=payload)

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
    def get_stats(self, vps_ids):
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

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def change_pass(self, payload):
        linked_id = payload.get('linked_id')
        url = f"{self.base_url}/system/vpss/{linked_id}/change_pass"
        response = requests.post(url, headers=self.headers, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            # Raise an HTTP error for non-200 status codes
            response.raise_for_status()

    def refund(self, vps_id):
        return True

    def stat(self, vps_id):
        url = f"{VIRTUALIZOR_CONFIG.MANAGER_URL}/system/vpss/stat"
        payload = {'vps_ids': [vps_id]}
        response = requests.post(url, headers=self.headers, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            stat = response.json().get(str(vps_id))
            return stat
        else:
            return {}


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
    def delete(self, vps_id):
        url = f"{self.base_url}/api/vps/delete/"
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
    def update_vps_end_time(self, linked_id, end_time):
        url = f"{self.base_url}/api/vps/update_vps_end_time/"
        response = requests.post(url, headers=self.headers, json={'linked_id': linked_id, 'end_time': end_time})

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

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def change_pass(self, payload):

        url = f"{self.base_url}/api/vps/change_pass/"
        response = requests.post(url, headers=self.headers, json={
            'linked_ids': [payload.get('linked_id')],
            'password': payload.get('password')
        })

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            # Raise an HTTP error for non-200 status codes
            response.raise_for_status()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def change_hostname(self, vps_id, payload):
        url = f"{self.base_url}/api/vps/{vps_id}/update_info/"
        payload['linked_id'] = vps_id
        response = requests.post(url, headers=self.headers, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            # Raise an HTTP error for non-200 status codes
            response.raise_for_status()

    # @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    # def refund(self, vps_id):
    #     url = f"{self.base_url}/api/vps/refund/"
    #     response = requests.post(url, headers=self.headers, json={'linked_ids': [vps_id]})
    #
    #     # Check if the request was successful
    #     if response.status_code == 200:
    #         return response.json()
    #     else:
    #         # Raise an HTTP error for non-200 status codes
    #         response.raise_for_status()
