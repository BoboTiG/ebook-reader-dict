from typing import Dict, List

import requests

url = "https://{0}.wiktionary.org/w/api.php?action=query&meta=siteinfo&siprop=namespaces&format=json"

results: Dict[str, List[str]] = {}
locales = ("ca", "de", "el", "en", "es", "fr", "it", "no", "pt", "ru", "sv")

for locale in locales:
    result_discard_last: List[str] = []
    langurl = url.format(locale)
    r = requests.get(langurl)
    json = r.json()
    namespaces = json["query"]["namespaces"]
    for key, namespace in namespaces.items():
        if n := namespace["*"]:
            if namespace["canonical"] in ["File", "Category"]:
                result_discard_last.append(n)
    results[locale] = result_discard_last

print("namespaces =", end=" ")
print(results)
