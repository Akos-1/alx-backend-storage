#!/usr/bin/env python3

"""
This module defines a Cache class that interacts with Redis.
"""

import redis
import uuid
import functools
from typing import Callable, Union


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a
    function in Redis lists.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store input and output history in Redis lists.

        Args:
            self: The instance of the class.
            *args: Positional arguments passed to the method.
            **kwargs: Keyword arguments passed to the method.

        Returns:
            Any: The result of the original method call.
        """
        # Get the qualified name of the method
        key = method.__qualname__

        # Store input arguments
        input_key = key + ":inputs"
        self._redis.rpush(input_key, str(args))

        # Execute the original method to retrieve the output
        output = method(self, *args, **kwargs)

        # Store output
        output_key = key + ":outputs"
        self._redis.rpush(output_key, str(output))

        return output

    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to increment call count and call the original method.

        Args:
            self: The instance of the class.
            *args: Positional arguments passed to the method.
            **kwargs: Keyword arguments passed to the method.

        Returns:
            Any: The result of the original method call.
        """
        # Get the qualified name of the method
        key = method.__qualname__
        # Increment the count for the method
        self._redis.incr(key)
        # Call the original method and return its result
        return method(self, *args, **kwargs)

    return wrapper


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

    @call_history
    @count_calls
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

    def replay(self, method: Callable):
        """
        Display the history of calls of a particular function.

        Args:
            method (Callable): The method for which the history
            of calls is to be displayed.
        """
        # Get the qualified name of the method
        key = method.__qualname__

        # Retrieve input and output keys from Redis
        input_key = key + ":inputs"
        output_key = key + ":outputs"

        # Get the number of calls made to the method
        num_calls = self._redis.llen(input_key)

        print(f"{key} was called {num_calls} times:")

        # Retrieve inputs and outputs from Redis
        inputs = self._redis.lrange(input_key, 0, -1)
        outputs = self._redis.lrange(output_key, 0, -1)

        # Display each call along with its input and output
        for args, output in zip(inputs, outputs):
            print(f"{key}(*{args.decode('utf-8')}) -> {output.decode('utf-8')}")

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
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

    # Test the decorated method
    for i in range(5):
        key = cache.store("Data")
        print(f"Stored data with key: {key}")

    # Display history of calls for the store method
    cache.replay(cache.store)
