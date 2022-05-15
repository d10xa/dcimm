import re
import shutil
import sys
from pathlib import Path
from typing import List

from dcimm.ChecksumFileLine import ChecksumFileLine
from dcimm.CopyItem import CopyItem
from dcimm.functions import list_files, make_copy_items


def main():
    src_dir = sys.argv[1]
    dest_dir = sys.argv[2]
    for dir, files in list_files(src_dir):
        sumfile = Path(dir, f'{dir.name}.sha256')
        print(sumfile)

        lines: List[ChecksumFileLine] = []
        if sumfile.exists():
            with open(sumfile, 'r') as f:
                lines = parse_checksum_file(f.readlines())
        file_to_sumfileline = {i.name: i for i in lines}

        copy_items: list[CopyItem] = make_copy_items(files, Path(dest_dir))
        print(f'copy_items: {copy_items}')

        for c in copy_items:
            if c.to_file.exists():
                raise Exception(f'file {c.to_file.absolute()} already exists')

        for c in copy_items:
            if c.from_file == sumfile:
                print(f'original sumfile ignored (ok): {sumfile}')
                continue
            c.to_file.parent.mkdir(parents=True, exist_ok=True)
            new_sumfile=Path(c.to_file.parent, f'{c.to_file.parent.name}.sha256')
            shutil.copy2(c.from_file, c.to_file)
            if c.from_file.name in file_to_sumfileline:
                line = file_to_sumfileline.get(c.from_file.name)
                if line:
                    with open(new_sumfile, 'a+') as newfile:
                        newfile.write(f'{line.raw}\n')
                else:
                    print(f'NOT FOUND CHECKSUM: {c.from_file.name}')


def parse_checksum_file(strs: List[str]) -> List[ChecksumFileLine]:
    res = []
    pattern = re.compile(r'([a-f0-9]{64})\s{1,2}\*?(.+)')
    for line in strs:
        line = line.rstrip('\n')
        match = pattern.search(line)
        if match:
            res.append(ChecksumFileLine(match.group(1), match.group(2), line))
        else:
            res.append(ChecksumFileLine(None, None, line))
    return res


if __name__ == '__main__':
    main()
