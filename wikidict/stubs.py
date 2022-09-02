"""Type annotations."""
from collections import namedtuple
from typing import Dict, List, Tuple, Union

SubDefinitions = Union[str, Tuple[str, ...]]
Definitions = Union[str, Tuple[str, ...], Tuple[SubDefinitions, ...]]
Parts = Tuple[str, ...]
Pronunciations = List[str]
Variants = Dict[str, List[str]]
Word = namedtuple("Word", "pronunciations, gender, etymology, definitions, variants")
Words = Dict[str, Word]
Groups = Dict[str, Words]
