import os
import time

import requests
from dotenv import load_dotenv
from loguru import logger

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("RIOT_API_KEY")
HEADERS = {"X-Riot-Token": API_KEY}


def riot_request(url, params=None, max_retries=5):
    """
    Makes an HTTP GET request to the Riot API with retry and rate limit handling.

    Retries automatically on HTTP 429 using the Retry-After header.

    Args:
        url (str): Riot API endpoint.
        params (dict, optional): Query parameters.
        max_retries (int): Max retry attempts on failure.

    Returns:
        dict: The parsed JSON response.
    """
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=HEADERS, params=params)

            if response.status_code == 200:
                return response.json()

            elif response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 1))
                logger.warning(
                    f"[429] Rate limited. Sleeping for {retry_after}s (attempt {attempt}/{max_retries})"
                )
                time.sleep(retry_after)

            else:
                response.raise_for_status()

        except requests.RequestException as e:
            logger.warning(
                f"[{type(e).__name__}] Request failed (attempt {attempt}/{max_retries}): {e}"
            )
            time.sleep(1)

    raise RuntimeError(f"Failed to fetch Riot API after {max_retries} attempts: {url}")
