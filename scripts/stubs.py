"""Type annotations."""
from collections import namedtuple
from typing import Dict, Tuple, Union

Definitions = Union[str, Tuple[str, ...]]
Parts = Tuple[str, ...]
Word = namedtuple("Word", "pronunciations, genre, etymology, definitions, variants")
Words = Dict[str, Word]
