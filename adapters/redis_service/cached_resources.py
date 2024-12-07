import json

import requests

from adapters.kafka_adapter import make_kafka_publisher
from adapters.redis_service.__base__ import CachedResource, RedisService
from config import KafkaNotifierConfig
from core import settings


class CachedPlan(CachedResource):
    key_name = "cached_plans"

    def __init__(self):
        redis_uri = settings.REDIS_CONFIG.REDIS_URI
        data_url = settings.VIRTUALIZOR_CONFIG.MANAGER_URL + "/system/plans"
        auth_header = {"x-api-key": settings.VIRTUALIZOR_CONFIG.API_KEY}
        ex = 60 * 60 * 24  # 24 hours
        super().__init__(redis_uri=redis_uri, data_url=data_url, auth_header=auth_header, ex=ex)

    def _pre_set(self, value):
        return sorted(value, key=lambda x: (x.get('cluster_id'), x.get('price')))


class AgenSyncObject:
    sync_type = 'sync_type'
    event_type = 'agen_sync'

    def __init__(self):
        self.kafka_config = KafkaNotifierConfig

    def get_sync_data(self):
        pass

    def sync(self):
        data = self.get_sync_data()
        publisher = make_kafka_publisher(KafkaNotifierConfig)
        publisher.publish(self.event_type, {
            'data': data,
            'sync_type': self.sync_type
        })


class CachedObject(RedisService):
    key_name = "object_key"

    def __init__(self):
        redis_uri = settings.REDIS_CONFIG.REDIS_URI
        ex = 60 * 60 * 24  # 24 hours
        super().__init__(redis_uri=redis_uri, ex=ex)

    def get(self, sub_key=''):
        key_name = self.key_name
        if sub_key:
            key_name = f"{key_name}:{sub_key}"

        value = super().get(key_name)
        return value

    def set(self, value, sub_key='', ex=None, px=None):
        key_name = self.key_name
        if sub_key:
            key_name = f"{key_name}:{sub_key}"

        super().set(key_name, value, ex, px)

    def get_all(self):
        pattern = f"{self.key_name}*"
        cursor = 0
        all_keys = []
        while True:
            cursor, keys = self.client.scan(cursor, match=pattern, count=100)
            all_keys.extend(keys)
            if cursor == 0:  # Exit when the scan is complete
                break

        all_keys = [key for key in all_keys if key == self.key_name or key.startswith(f"{self.key_name}:")]

        all_values = self.client.mget(all_keys)
        json_values = []
        for value in all_values:
            try:
                json_values.append(json.loads(value))
            except:
                json_values.append(value)
        return dict(zip(all_keys, json_values))

    def get_sync_data(self):
        data = self.get_all()
        return data


class CachedPlanInRegion(CachedObject, AgenSyncObject):
    key_name = "cached_plans_in_region"
    sync_type = 'REGION_PLAN'

    def set(self, value, sub_key='', ex=None, px=None):
        super().set(value, sub_key)
        self.sync()


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
