import re

from scripts_utils import get_content

ROOT_URL = "https://no.wiktionary.org"


def process_page(page_url: str) -> dict[str, str]:
    content = get_content(page_url)
    labels: dict[str, str] = {}

    for link in set(re.findall(r'title="(Mal:[^"]+)"', content)):
        if link.endswith("tema"):
            continue

        label_url = f"{ROOT_URL}/w/index.php?title={link}"
        code = get_content(f"{label_url}&action=raw").replace("''", "").replace("[[", "").replace("]]", "")
        value = (re.findall(r"\(([^\)]+)\)", code) or re.findall(r"kontekst=([^|]+)\|", code))[0]
        if "|" in value:
            value = value.split("|")[1]
        labels[link.split(":")[1]] = value

    return labels


labels = process_page(f"{ROOT_URL}/wiki/Kategori:Temamaler")
print("labels = {")
for key, value in sorted(labels.items()):
    print(f'    "{key}": "{value}",')
print(f"}}  # {len(labels):,}")
