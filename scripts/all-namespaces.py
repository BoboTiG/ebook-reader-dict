from typing import Dict, List

from scripts_utils import get_content

url = "https://{0}.wiktionary.org/w/api.php?action=query&meta=siteinfo&siprop=namespaces&format=json"

results: Dict[str, List[str]] = {}
locales = ("ca", "de", "el", "en", "es", "fr", "it", "no", "pt", "ru", "sv")

for locale in locales:
    result_discard_last: List[str] = []
    json = get_content(url.format(locale), as_json=True)
    namespaces = json["query"]["namespaces"]
    for key, namespace in namespaces.items():
        if n := namespace["*"]:
            if namespace["canonical"] in ["File", "Category"]:
                result_discard_last.append(n)
    results[locale] = result_discard_last

print("namespaces =", end=" ")
print(results)
