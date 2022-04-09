from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CopyItem:
    from_file: Path
    to_file: Path
