#!/usr/bin/env python3

import requests
import redis
import time
from typing import Dict

# Initialize Redis connection
redis_client = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL and returns it, while
    caching the result and tracking the number of accesses.

    Args:
        url (str): The URL of the webpage.

    Returns:
        str: The HTML content of the webpage.
    """
    # Check if the URL content is cached
    cached_content = redis_client.get(url)
    if cached_content:
        # Increment the count of accesses for this URL
        redis_client.incr(f"count:{url}")
        return cached_content.decode('utf-8')

    # Fetch the HTML content from the URL
    response = requests.get(url)
    html_content = response.text

    # Cache the HTML content with an expiration time of 10 seconds
    redis_client.setex(url, 10, html_content)

    # Track the count of accesses for this URL
    redis_client.incr(f"count:{url}")

    return html_content


# Test the function
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"
    start_time = time.time()
    for _ in range(5):
        content = get_page(url)
        print(f"HTML Content Length: {len(content)}")
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time} seconds")
