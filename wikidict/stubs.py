"""Type annotations."""

from typing import NamedTuple

SubDefinition = str | tuple[str, ...]
Definition = str | tuple[str, ...] | tuple[SubDefinition, ...]
Definitions = dict[str, list[Definition]]
Parts = tuple[str, ...]
Variants = dict[str, list[str]]


class Word(NamedTuple):
    pronunciations: list[str]
    genders: list[str]
    etymology: list[Definition]
    definitions: Definitions
    variants: list[str]


Words = dict[str, Word]
Groups = dict[str, Words]
