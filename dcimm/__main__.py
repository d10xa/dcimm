import shutil
import sys
from pathlib import Path
from typing import List

from dcimm.functions import list_files, make_copy_items


def main():
    src_dir = sys.argv[1]
    dest_dir = sys.argv[2]
    files: List[Path] = list_files(src_dir)
    copy_items = make_copy_items(files, Path(dest_dir))
    for c in copy_items:
        if c.to_file.exists():
            raise Exception(f'file {c.to_file.absolute()} already exists')

    for c in copy_items:
        c.to_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(c.from_file, c.to_file)


if __name__ == '__main__':
    main()
