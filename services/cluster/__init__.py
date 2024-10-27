import requests

from config import VIRTUALIZOR_CONFIG


class ClusterManager:
    def test_cluster(self, ip, api_key, api_pass, user_api_key, user_api_pass):
        url = VIRTUALIZOR_CONFIG.MANAGER_URL + "/system/clusters/test"
        data = {
            "ip": ip,
            "api_key": api_key,
            "api_pass": api_pass,
            "user_api_key": user_api_key,
            "user_api_pass": user_api_pass
        }

        header = {"x-api-key": VIRTUALIZOR_CONFIG.API_KEY}
        response = requests.post(url, json=data, headers=header)

        if response.status_code == 200:
            return True
        else:
            return False

    def create_cluster(self, name, ip, api_key, api_pass, user_api_key, user_api_pass):
        url = VIRTUALIZOR_CONFIG.MANAGER_URL + "/system/clusters"
        data = {
            "name": name,
            "ip": ip,
            "api_key": api_key,
            "api_pass": api_pass,
            "user_api_key": user_api_key,
            "user_api_pass": user_api_pass
        }

        header = {"x-api-key": VIRTUALIZOR_CONFIG.API_KEY}
        response = requests.post(url, json=data, headers=header)

        if response.status_code == 200:
            return response.json()
        else:
            return False
