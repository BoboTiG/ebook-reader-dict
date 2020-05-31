"""Type annotations."""
from typing import Dict, List, Tuple, Union

Definitions = Union[str, Tuple[str, ...]]
Word = Tuple[str, str, List[Definitions]]
Words = Dict[str, Word]
