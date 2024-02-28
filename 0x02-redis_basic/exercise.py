#!/usr/bin/env python3

"""
This module defines a Cache class that interacts with Redis.
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    A class for caching data using Redis.
    """

    def __init__(self):
        """
        Initializes the Cache object and connects to Redis.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis with a randomly generated key and returns the key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The randomly generated key used to store the data in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


if __name__ == "__main__":
    cache = Cache()
    key = cache.store("Hello, world!")
    print("Stored data with key:", key)
