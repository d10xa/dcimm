from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ChecksumFileLine:
    sum: Optional[str]  # TODO rename
    name: Optional[str]
    raw: str
