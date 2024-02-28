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

    def get(self, key: str, fn: Callable = None
            ) -> Union[str, bytes, int, float, None]:
        """
        Retrieves data from Redis using the given key and
        applies the optional conversion function.

        Args:
            key (str): The key associated with the data in Redis.
            fn (Callable, optional): A callable function
            to convert the retrieved data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data,
            optionally converted by fn.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Convenience method to retrieve data as a string
        from Redis using the given key.

        Args:
            key (str): The key associated with the data in Redis.

        Returns:
            Union[str, None]: The retrieved data as a string,
            or None if the key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Convenience method to retrieve data as an integer
        from Redis using the given key.

        Args:
            key (str): The key associated with the data in Redis.

        Returns:
            Union[int, None]: The retrieved data as an integer,
            or None if the key does not exist.
        """
        return self.get(key, fn=int)


if __name__ == "__main__":
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value
