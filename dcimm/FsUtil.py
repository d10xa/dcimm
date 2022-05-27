import shutil
from pathlib import Path


class FsUtil:

    def mk_dir(self, path: Path) -> None:
        pass

    def copy2(self, src: Path, dst: Path) -> None:
        pass

    def append_line(self, file: Path, line: str) -> None:
        pass

    @staticmethod
    def make(dry_run: bool) -> 'FsUtil':
        if dry_run:
            return FsUtilDry()
        else:
            return FsUtilReal()


class FsUtilDry(FsUtil):
    def mk_dir(self, path: Path) -> None:
        if not path.exists():
            print(f'dry-run: mkdir {path}')

    def copy2(self, src: Path, dst: Path) -> None:
        print(f'dry-run: copy {src} to {dst}')

    def append_line(self, file: Path, line: str) -> None:
        print(f'dry-run: append line {file}: {line}')


class FsUtilReal(FsUtil):
    def mk_dir(self, path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)

    def copy2(self, src: Path, dst: Path) -> None:
        shutil.copy2(src, dst)

    def append_line(self, file: Path, line: str) -> None:
        with open(file, 'a+') as newfile:
            newfile.write(f'{line}\n')
