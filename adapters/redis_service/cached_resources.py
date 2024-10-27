import requests

from adapters.redis_service.__base__ import CachedResource
from core import settings


class CachedPlan(CachedResource):
    key_name = "cached_plans"

    def __init__(self):
        redis_uri = settings.REDIS_CONFIG.REDIS_URI
        data_url = settings.VIRTUALIZOR_CONFIG.MANAGER_URL + "/system/plans"
        auth_header = {"x-api-key": settings.VIRTUALIZOR_CONFIG.API_KEY}
        ex = 60 * 60 * 24  # 24 hours
        super().__init__(redis_uri=redis_uri, data_url=data_url, auth_header=auth_header, ex=ex)


class CachedOS(CachedResource):
    key_name = "cached_oses"

    def __init__(self):
        redis_uri = settings.REDIS_CONFIG.REDIS_URI
        data_url = settings.VIRTUALIZOR_CONFIG.MANAGER_URL + "/system/oses"
        auth_header = {"x-api-key": settings.VIRTUALIZOR_CONFIG.API_KEY}
        ex = 60 * 60 * 24  # 24 hours
        super().__init__(redis_uri=redis_uri, data_url=data_url, auth_header=auth_header, ex=ex)


class CachedServer(CachedResource):
    key_name = "cached_servers"

    def __init__(self):
        redis_uri = settings.REDIS_CONFIG.REDIS_URI
        data_url = settings.VIRTUALIZOR_CONFIG.MANAGER_URL + "/system/servers"
        auth_header = {"x-api-key": settings.VIRTUALIZOR_CONFIG.API_KEY}
        ex = 60 * 60 * 24  # 24 hours
        super().__init__(redis_uri=redis_uri, data_url=data_url, auth_header=auth_header, ex=ex)


class CachedServerGroup(CachedResource):
    key_name = "cached_server_groups"

    def __init__(self):
        redis_uri = settings.REDIS_CONFIG.REDIS_URI
        data_url = settings.VIRTUALIZOR_CONFIG.MANAGER_URL + "/system/server_groups"
        auth_header = {"x-api-key": settings.VIRTUALIZOR_CONFIG.API_KEY}
        ex = 60 * 60 * 24  # 24 hours
        super().__init__(redis_uri=redis_uri, data_url=data_url, auth_header=auth_header, ex=ex)

    def update(self, id, data):
        data_url = settings.VIRTUALIZOR_CONFIG.MANAGER_URL + "/system/server_groups/update"
        data["id"] = id
        fields = ["country", "name", "id"]
        data = {field: data.get(field) for field in fields}
        res = requests.post(data_url, json=data, headers=self.auth_header)
        self.delete()
        return self.get()


class CachedVpsBackup(CachedResource):
    key_name = "cached_vps_backup"

    def __init__(self):
        redis_uri = settings.REDIS_CONFIG.REDIS_URI
        data_url = settings.VIRTUALIZOR_CONFIG.MANAGER_URL + "/system/vpss/<vps_id>/list_backup"
        auth_header = {"x-api-key": settings.VIRTUALIZOR_CONFIG.API_KEY}
        ex = 60  # 24 hours
        super().__init__(redis_uri=redis_uri, data_url=data_url, auth_header=auth_header, ex=ex)

    def _fetch_from_api(self, retry_count, sub_key=''):
        data_url = self.data_url.replace("<vps_id>", sub_key)
        while retry_count > 0:
            try:
                response = self._make_api_call(data_url)
                if response:
                    return response
            except Exception as e:
                print(f"Error fetching data from API: {e}")
            retry_count -= 1
        return None


if __name__ == "__main__":
    # plan = CachedPlan()
    # print(plan.get())
    # plan.delete()
    #
    # os = CachedOS()
    # print(os.get())
    #
    # server = CachedServer()
    # print(server.get())

    # server = CachedServer()
    # server.delete()
    # print(server.get())

    # server_group = CachedServerGroup()
    # server_group.delete()
    # print(server_group.get())

    vps_backup = CachedVpsBackup()
    print(vps_backup.get(1249))
