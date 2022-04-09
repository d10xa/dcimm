import os
import re
from pathlib import Path
from typing import Optional, List

from dcimm.CopyItem import CopyItem
from dcimm.LocalDateTime import LocalDateTime


def make_copy_items(src_files: List[Path], dest_dir: Path) -> List[CopyItem]:
    assert dest_dir.is_dir() or not dest_dir.exists()
    res: List[CopyItem] = []
    for file in src_files:
        ldt = filename_to_localdatetime(file.name)
        if ldt:
            res.append(CopyItem(file, Path(dest_dir, ldt.yyyymm(), file.name)))
        else:
            res.append(CopyItem(file, Path(dest_dir, 'other', file.name)))
    return res


def list_files(path: str):
    res = []
    for filename in os.listdir(path):
        p = Path(path, filename)
        if p.is_file() and not p.is_symlink():
            res.append(p)
    return res


def list_files_recursive(path: str):
    res = []
    for root, dirs, files in os.walk(path, topdown=False, followlinks=False):
        for file in files:
            p = Path(root, file)
            if p.is_file() and not p.is_symlink():
                res.append(p)
    return res


pattern = re.compile(r'(20\d{2})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})*.jpg')


def filename_to_localdatetime(filename: str) -> Optional[LocalDateTime]:
    match = re.search(pattern, filename)
    if match:
        year, month, day, hour, minute, second = match.groups()
        return LocalDateTime(year, month, day, hour, minute, second)
    else:
        return None
