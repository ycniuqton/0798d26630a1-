import requests

from core import settings


class VirtualizorManager:
    def __init__(self):
        self.url = settings.VIRTUALIZOR_CONFIG.MANAGER_URL
        self.api_key = settings.VIRTUALIZOR_CONFIG.API_KEY
        self.headers = {"x-api-key": self.api_key}

    def restore_vps(self, vps_id, abs_path):
        url = f"{self.url}/system/vpss/{vps_id}/restore"
        data = {"abs_path": abs_path}
        retry_count = 3
        while retry_count > 0:
            try:
                response = requests.post(url, headers=self.headers, json=data)
                if response.status_code == 200:
                    return True
            except Exception as e:
                print(f"Error fetching data from API: {e}")
            retry_count -= 1
        return False

    def set_price(self, plan_id, price):
        url = f"{self.url}/system/plans/set_price"
        data = {
            "plan_id": plan_id,
            "amount": price
        }
        retry_count = 3
        while retry_count > 0:
            try:
                response = requests.post(url, headers=self.headers, json=data)
                if response.status_code == 200:
                    return True
            except Exception as e:
                print(f"Error fetching data from API: {e}")
            retry_count -= 1
        return False
