from adapters.redis_service import CachedResource, RedisService
from core import settings


class CachedFullServerGroup(CachedResource):
    key_name = "cached_full_server_groups"

    def __init__(self):
        redis_uri = settings.REDIS_CONFIG.REDIS_URI
        data_url = settings.VIRTUALIZOR_CONFIG.MANAGER_URL + "/system/server_groups/load"
        auth_header = {"x-api-key": settings.VIRTUALIZOR_CONFIG.API_KEY}
        ex = 3600  # 24 hours
        super().__init__(redis_uri=redis_uri, data_url=data_url, auth_header=auth_header, ex=ex)


class CachedServerGroupConfig(RedisService):
    key_name = "cached_server_group_configs"

    def __init__(self):
        redis_uri = settings.REDIS_CONFIG.REDIS_URI
        super().__init__(redis_uri=redis_uri, ex=3600)
        self.cached_server_group = CachedFullServerGroup()

    def get(self):
        data = super().get(self.key_name)
        data = None
        if not data:
            data = self.cached_server_group.get()
        for k, v in data.items():
            if 'is_locked' not in v:
                v['is_locked'] = False
            if not v.get('servers'):
                continue
            # workaround for localhost
            if isinstance(v['servers'], list):
                v['servers'] = {i: {"name": i, "is_locked": False} for i in v['servers']}
            for server_id, server in v['servers'].items():
                if isinstance(server, dict):
                    continue
                else:
                    v['servers'][server_id] = {
                        "name": server,
                        "is_locked": False
                    }
        self.set(data, ex=3600)
        return data

    def set(self, value, ex=None, px=None):
        super().set(self.key_name, value, ex, px)

    def get_locked(self, group_id):
        group_configs = self.get()
        group = group_configs.get(str(group_id))
        if not group or not group.get('is_locked'):
            return False

        for server_id, server in group.get('servers').items():
            if server.get('is_locked'):
                return server_id

        return False

