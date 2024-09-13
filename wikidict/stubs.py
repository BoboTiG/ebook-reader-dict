"""Type annotations."""

from typing import NamedTuple

SubDefinitions = str | tuple[str, ...]
Definitions = str | tuple[str, ...] | tuple[SubDefinitions, ...]
Parts = tuple[str, ...]
Variants = dict[str, list[str]]


class Word(NamedTuple):
    pronunciations: list[str]
    genders: list[str]
    etymology: list[Definitions]
    definitions: list[Definitions]
    variants: list[str]

    @classmethod
    def empty(cls) -> "Word":
        return cls([], [], [], [], [])


Words = dict[str, Word]
Groups = dict[str, Words]
