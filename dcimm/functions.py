import os
import re
from datetime import datetime
from pathlib import Path
from typing import Generator
from typing import List
from typing import Optional
from typing import Tuple

from exif import Image

from dcimm.ChecksumFileLine import ChecksumFileLine
from dcimm.CopyItem import CopyItem
from dcimm.FsUtil import FsUtil


def flat_map(f, xs):
    ys = []
    for x in xs:
        ys.extend(f(x))
    return ys


def run(src: List[str], dest: str, dry_run: bool):
    fs_util: FsUtil = FsUtil.make(dry_run=dry_run)
    for dir, files in flat_map(list_files, src):
        sumfile = Path(dir, f'{dir.name}.sha256')
        print(sumfile)

        lines: List[ChecksumFileLine] = []
        if sumfile.exists():
            with open(sumfile, 'r') as f:
                lines = parse_checksum_file(f.readlines())
        file_to_sumfileline = {i.name: i for i in lines}

        copy_items: list[CopyItem] = make_copy_items(files, Path(dest))
        print(f'copy_items: {copy_items}')

        for c in copy_items:
            if c.to_file.exists():
                raise Exception(f'file {c.to_file.absolute()} already exists')

        for c in copy_items:
            if c.from_file == sumfile:
                print(f'original sumfile ignored (ok): {sumfile}')
                continue
            fs_util.mk_dir(c.to_file.parent)
            new_sumfile=Path(c.to_file.parent, f'{c.to_file.parent.name}.sha256')
            fs_util.copy2(c.from_file, c.to_file)
            if c.from_file.name in file_to_sumfileline:
                line = file_to_sumfileline.get(c.from_file.name)
                if line:
                    fs_util.append_line(new_sumfile, line.raw)
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


def make_copy_items(src_files: List[Path], dest_dir: Path) -> List[CopyItem]:
    assert dest_dir.is_dir() or not dest_dir.exists()
    res: List[CopyItem] = []
    file: Path
    for file in src_files:
        ldt: Optional[datetime] = file_to_exif_datetime(file)
        if ldt:
            res.append(CopyItem(file, Path(dest_dir, format_yyyymm(ldt), file.name)))
        else:
            res.append(CopyItem(file, Path(dest_dir, 'other', file.name)))
    return res


def list_files(path: str) -> Generator[Tuple[Path, List[Path]], None, None]:
    files: List[Path] = []
    for filename in os.listdir(path):
        p = Path(path, filename)
        if p.is_file() and not p.is_symlink():
            files.append(p)
    yield Path(path), files


def list_files_recursive(path: str) -> Generator[Tuple[Path, List[Path]], None, None]:
    for root, dirs, files in os.walk(path, topdown=False, followlinks=False):
        for file in files:
            p = Path(root, file)
            if p.is_file() and not p.is_symlink():
                yield p


pattern = re.compile(r'(20\d{2})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})*.jpg')


def file_to_localdatetime(file: Path) -> Optional[datetime]:
    match = re.search(pattern, file.name)
    if match:
        year, month, day, hour, minute, second = match.groups()
        return datetime(
            int(year.lstrip('0')),
            int(month.lstrip('0')),
            int(day.lstrip('0')),
            int(hour.lstrip('0')),
            int(minute.lstrip('0')),
            int(second.lstrip('0'))
        )
    else:
        return None


def format_yyyymmdd(d: datetime):
    return f'{d.year}-{d.month:02d}-{d.day:02d}'


def format_yyyymm(d: datetime):
    return f'{d.year}-{d.month:02d}'


def file_to_exif_datetime(file) -> Optional[datetime]:
    if not file.name.lower().endswith(('.jpg', '.mov', '.mp4')):
        return None

    with open(file, 'rb') as image_file:
        my_image = Image(image_file)

        d = my_image.datetime_original or my_image.datetime
        if d:
            return datetime.strptime(d, '%Y:%m:%d %H:%M:%S')
        else:
            return None
