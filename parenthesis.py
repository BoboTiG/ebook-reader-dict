# File: parenthesis.py
import json
import re
import sys

with open(sys.argv[1]) as fh:
    words = json.load(fh)

seen = set()
pattern = re.compile(r"(\([A-Z]+[^\)]+\))")
for word, definitions in words.items():
    for definition in definitions[-1]:
        if isinstance(definition, str):
            for m in pattern.findall(definition):
                if m not in seen:
                    print(m, repr(word))
                    seen.add(m)
        else:
            for subdef in definition:
                for m in pattern.findall(subdef):
                    if m not in seen:
                        print(m, repr(word))
                        seen.add(m)

 !! Missing 'u' template support for word '-ing'
 !! Missing 'compound' template support for word 'hjemmeværn'
 !! Missing 'trad' template support for word 'limnologi'
 !! Missing 'trad' template support for word 'ondulere'
 !! Missing 'u' template support for word 'ris'
 !! Missing 'suffix' template support for word 'nordisk'
 !! Missing 'u' template support for word 'vandfald'


parts =    "compound|hjemme|værn".split('|')
' + '.join(parts[1:])
