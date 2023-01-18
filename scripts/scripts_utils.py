from time import sleep
from typing import Any, Dict

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


def get_content(
    url: str, max_retries: int = 5, sleep_time: int = 5, as_json: bool = False
) -> str | Dict[str, Any]:
    """Fetch given *url* content with retries mechanism."""
    retry = 0
    while retry < max_retries:
        try:
            with requests.get(url, timeout=10) as req:
                req.raise_for_status()
                return req.json() if as_json else req.text
        except TimeoutError:
            sleep(sleep_time)
            retry += 1
        except RequestException as err:
            resp = err.response
            if resp.status_code == 404:
                return ""
            wait_time = 1
            if resp is not None and resp.status_code == 429:
                wait_time = int(resp.headers.get("retry-after") or "1")
            sleep(wait_time * sleep_time)
            retry += 1
    raise RuntimeError(f"Sorry, too many tries [{retry}] for {url!r}")


def get_soup(url: str) -> BeautifulSoup:
    page = get_content(url)
    return BeautifulSoup(page, features="html.parser")
