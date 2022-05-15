from dcimm.functions import run
import argparse


def main():
    parser = argparse.ArgumentParser(prog='dcimm')
    subparsers = parser.add_subparsers(help='sub-command help')
    parser_cp_sort = subparsers.add_parser(name='cp-sort', help='cp-sort help')
    parser_cp_sort.add_argument('--dry-run', action=argparse.BooleanOptionalAction, default=False)
    parser_cp_sort.add_argument('src', type=str, nargs='+')
    parser_cp_sort.add_argument('dest', type=str)
    args = parser.parse_args()
    run(src=args.src, dest=args.dest, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
