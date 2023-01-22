from typing import Dict, List

from scripts_utils import get_content

url = "https://{0}.wiktionary.org/w/api.php?action=query&meta=siteinfo&siprop={1}&format=json"

# https://en.wiktionary.org/wiki/Wiktionary:Namespace
ids = {6, 14}  # File, and Category

results: Dict[str, List[str]] = {}
locales = ("ca", "de", "el", "en", "es", "fr", "it", "no", "pt", "ru", "sv")

for locale in locales:
    result_discard_last: List[str] = []
    for kind in ("namespaces", "namespacealiases"):
        json = get_content(url.format(locale, kind), as_json=True)
        data = json["query"][kind]
        if kind == "namespaces":
            for id_ in ids:
                result_discard_last.append(data[str(id_)]["*"])
        else:
            for namespace in data:
                if namespace["id"] in ids:
                    result_discard_last.append(namespace["*"])
        results[locale] = sorted(result_discard_last)

print("namespaces =", end=" ")
print(results)
