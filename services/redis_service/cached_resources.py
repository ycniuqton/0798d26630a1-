import requests
from __base__ import CachedResource
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


if __name__ == "__main__":
    plan = CachedPlan()
    print(plan.get())
    # plan.delete()

    os = CachedOS()
    print(os.get())

    server = CachedServer()
    print(server.get())

