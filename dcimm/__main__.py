import sys

from dcimm.functions import run


def main():
    src_dir = sys.argv[1]
    dest_dir = sys.argv[2]
    run(src_dir, dest_dir)


if __name__ == '__main__':
    main()
