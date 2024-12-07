import json

import redis
import requests


class RedisService:
    def __init__(self, host='localhost', port=6379, db=0, password=None, redis_uri=None, ex=None, px=None):
        """
        Initializes the Redis connection.
        """
        if redis_uri:
            self.client = redis.Redis.from_url(redis_uri, decode_responses=True)
        else:
            self.client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True  # Ensures that responses are in string format
            )

        self.ex = ex
        self.px = px

    def set(self, key, value, ex=None, px=None):
        """
        Set a value in Redis.

        :param key: The key under which the value should be stored.
        :param value: The value to store.
        :param ex: Set the specified expire time, in seconds.
        :param px: Set the specified expire time, in milliseconds.
        :return: True if the key was set, otherwise False.
        """
        value = json.dumps(value)
        if not ex and self.ex:
            ex = self.ex
        if not px and self.px:
            px = self.px
        return self.client.set(key, value, ex=ex, px=px)

    def set_all(self, data):
        data = {key: json.dumps(value) for key, value in data.items()}
        return self.client.mset(data)

    def get(self, key):
        """
        Get a value from Redis.

        :param key: The key whose value needs to be fetched.
        :return: The value stored under the key, or None if the key doesn't exist.
        """
        try:
            return json.loads(self.client.get(key))
        except:
            return self.client.get(key)

    def delete(self, key):
        """
        Delete a key from Redis.

        :param key: The key to delete.
        :return: The number of keys that were removed.
        """
        return self.client.delete(key)

    def clear_cache_by_group(self, group):
        """
        Delete all keys that start with the specified group prefix.

        :param group: The group prefix for keys to delete.
        :return: The number of keys that were removed.
        """
        keys = self.client.keys(f"{group}*")
        if keys:
            return self.client.delete(*keys)
        return 0


class CachedResource(RedisService):
    def __init__(self, host=None, port=None, db=None, password=None, data_url=None, auth_header=None,
                 redis_uri=None, retry_count=3, ex=None, px=None):

        self.data_url = data_url
        self.auth_header = auth_header or {}
        self.redis_uri = redis_uri
        self.retry_count = retry_count
        super().__init__(host, port, db, password, redis_uri, ex, px)

    def get(self, sub_key=''):
        """
        Get the value from Redis. If it doesn't exist, fetch from an API.

        :param retry_count: The number of times to retry the API call.
        :return: The value retrieved from cache or API.
        """
        key_name = f"{self.key_name}:{sub_key}"
        value = super().get(key_name)
        if value is None:
            value = self._fetch_from_api(retry_count=self.retry_count, sub_key=sub_key)
            if value is not None:
                self.set(key_name, self._pre_set(value))
        return value

    def _pre_set(self, value):
        return value

    def set(self, key_name, value, ex=None, px=None):
        """
        Set the value in Redis.

        :param value: The value to store.
        :param ex: Set the specified expire time, in seconds.
        :param px: Set the specified expire time, in milliseconds.
        """
        super().set(key_name, value, ex, px)

    def delete(self, sub_key=''):
        """
        Delete the key from Redis.
        """
        key_name = f"{self.key_name}:{sub_key}"
        super().delete(key_name)

    def _fetch_from_api(self, retry_count, sub_key=''):
        """
        Fetch the value from an API. This method is meant to be overridden.

        :param retry_count: The number of times to retry the API call.
        :return: The value retrieved from the API, or None if the call failed.
        """
        while retry_count > 0:
            try:
                # Replace this with the actual API call logic
                response = self._make_api_call()
                if response:
                    return response
            except Exception as e:
                print(f"Error fetching data from API: {e}")
            retry_count -= 1
        return None

    def _make_api_call(self, url=None):
        if not url:
            url = self.data_url
        data = requests.get(url, headers=self.auth_header)
        if data.status_code == 200:
            return data.json()
        return None
