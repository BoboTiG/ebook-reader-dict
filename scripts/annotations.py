"""Internal type for type annotations."""
from typing import Dict, Generator, List, Tuple

Sections = Generator[str, None, None]
Word = Tuple[str, str, str, List[str]]
Words = Dict[str, Word]
WordList = Dict[str, str]
Groups = Dict[str, Words]
