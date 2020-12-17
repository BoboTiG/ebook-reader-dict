"""Type annotations."""
from collections import namedtuple
from typing import Dict, Tuple, Union

SubDefinitions = Union[str, Tuple[str, ...]]
Definitions = Union[str, Tuple[str, ...], Tuple[SubDefinitions, ...]]
Parts = Tuple[str, ...]
Word = namedtuple("Word", "pronunciations, genre, etymology, definitions, variants")
Words = Dict[str, Word]
