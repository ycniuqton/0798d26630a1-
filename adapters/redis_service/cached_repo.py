from adapters.redis_service.__base__ import CachedResource, RedisService
from core import settings
from home.models import Vps
from services.vps import VPSService


class CachedRepository(RedisService):
    prefix = "prefix"
    suffix = "suffix"

    def __init__(self):
        redis_uri = settings.REDIS_CONFIG.REDIS_URI
        ex = 60 * 60 * 24  # 24 hours
        super().__init__(redis_uri=redis_uri, ex=ex)

    def _key(self, key):
        return f"{self.prefix}:{key}:{self.suffix}"

    def get(self, key):
        return super().get(self._key(key))

    def set(self, key, value):
        super().set(self._key(key), value)


class CachedVpsStatRepository(CachedRepository):
    prefix = "vps"
    suffix = "repository"

    def reload(self, vps_ids=[]):
        base_url = settings.ADMIN_CONFIG.URL
        api_key = settings.ADMIN_CONFIG.API_KEY

        vps_service = VPSService(base_url, api_key)
        stats = vps_service.get_stat(vps_ids)
        for vps_id, stat in stats.items():
            self.set(vps_id, stat)


if __name__ == "__main__":
    vps_repo = CachedVpsStatRepository()
    vps_repo.set("1", {"name": "vps1"})
    print(vps_repo.get("1"))
    vps_repo.delete("1")
    print(vps_repo.get("1"))
    print(vps_repo.get("2"))
