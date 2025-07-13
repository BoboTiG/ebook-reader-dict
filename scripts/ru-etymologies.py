import contextlib
import sys
import threading
import time
from multiprocessing.pool import ThreadPool
from pathlib import Path

import requests
from scripts_utils import get_soup

LOCK = threading.Lock()
ROOT_URL = "https://ru.wiktionary.org"
START_URL = f"{ROOT_URL}/wiki/Категория:Шаблоны_этимологии"
NEXTPAGE_TEXT = "Следующая страница"


def process_page(page_url: str, etymologies: dict[str, str]) -> str:
    soup = get_soup(page_url)

    nextpage = ""
    nextpage_div = soup.find(id="mw-pages")
    last_link = nextpage_div.find_all("a")[-1]
    if NEXTPAGE_TEXT == last_link.text:
        nextpage = ROOT_URL + last_link.get("href")

    for li in soup.find("div", {"id": "mw-pages"}).find_all("li"):
        if (text := li.text).count(":") < 2:
            continue

        if (key := text.split(":")[2]) in etymologies:
            continue

        link = li.find("a")["href"]
        li_url = f"{ROOT_URL}{link}"
        etymologies[key] = li_url
    return nextpage


def get_current_etymologies() -> dict[str, str]:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from wikidict.lang.ru.etymologies import etymologies

    return etymologies


next_page_url = START_URL
etymologies = get_current_etymologies()

# Get all URL to download
while next_page_url:
    next_page_url = process_page(next_page_url, etymologies)

# Process additional pages
process_page(f"{ROOT_URL}/wiki/Категория:Шаблоны_этимологии_сложных_слов", etymologies)
process_page(f"{ROOT_URL}/wiki/Категория:Шаблоны_этимологии/gem-pro", etymologies)
process_page(f"{ROOT_URL}/wiki/Категория:Шаблоны_этимологии/trk-pro", etymologies)


def download(key: str, url: str) -> None:
    if not url.startswith("http"):
        return

    soup = get_soup(url).find("div", {"class": "mw-parser-output"})
    if not (content := soup.find("p", {"id": "mwAg"})):
        content = soup.find("section", {"id": "mwAQ"})

    with LOCK:
        etymologies[key] = content.text.strip()


with ThreadPool() as pool:
    iteration = 1
    while iteration < 5:
        with contextlib.suppress(requests.exceptions.HTTPError):
            pool.starmap(download, etymologies.items())
        if any(value.startswith("http") for value in etymologies.values()):
            time.sleep(5)
        else:
            break
        iteration += 1

print("etymologies = {")
for key, value in sorted(etymologies.items()):
    print(f"    {key!r}: {value!r},")
print(f"}}  # {len(etymologies):,}")
