import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from dcimm.functions import file_to_localdatetime
from dcimm.functions import format_yyyymmdd
from dcimm.functions import format_yyyymm


def test_filename_without_date():
    assert file_to_localdatetime(Path('test/abcd.jpg)')) is None


def test_filename_with_date():
    d = file_to_localdatetime(Path('test/20191230_235959.jpg)'))
    assert d == datetime(2019, 12, 30, 23, 59, 59)


def test_format_yyyymmdd():
    assert '2000-01-01' == format_yyyymmdd(datetime(2000, 1, 1, 1, 1, 1))


def test_format_yyyymm():
    assert '2000-01' == format_yyyymm(datetime(2000, 1, 1, 1, 1, 1))


if __name__ == '__main__':
    import pytest
    pytest.main()
