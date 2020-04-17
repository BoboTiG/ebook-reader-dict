"""Internal type for type annotations."""
from typing import Any, Dict, List, Tuple

# For xmltodict.parse() callback
Attribs = List[Tuple[str, Any]]
Item = Dict[str, Any]

Word = Tuple[str, str, str, List[str]]
Words = Dict[str, Word]
WordList = Dict[str, str]
Groups = Dict[str, Words]
