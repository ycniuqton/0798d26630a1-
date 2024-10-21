from adapters.redis_service import CachedResource, RedisService
from core import settings


class CachedCluster(CachedResource):
    key_name = "cached_cluster"

    def __init__(self):
        redis_uri = settings.REDIS_CONFIG.REDIS_URI
        data_url = settings.VIRTUALIZOR_CONFIG.MANAGER_URL + "/system/clusters"
        auth_header = {"x-api-key": settings.VIRTUALIZOR_CONFIG.API_KEY}
        ex = 3600  # 24 hours
        super().__init__(redis_uri=redis_uri, data_url=data_url, auth_header=auth_header, ex=ex)

