"""Type annotations."""

from typing import Dict, List, NamedTuple, Tuple, Union

SubDefinitions = Union[str, Tuple[str, ...]]
Definitions = Union[str, Tuple[str, ...], Tuple[SubDefinitions, ...]]
Parts = Tuple[str, ...]
Variants = Dict[str, List[str]]


class Word(NamedTuple):
    pronunciations: List[str]
    genders: List[str]
    etymology: List[Definitions]
    definitions: List[Definitions]
    variants: List[str]

    @classmethod
    def empty(cls) -> "Word":
        return cls([], [], [], [], [])


Words = Dict[str, Word]
Groups = Dict[str, Words]
