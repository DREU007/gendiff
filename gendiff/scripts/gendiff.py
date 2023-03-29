#!/usr/bin/env python3
import argparse
from gendiff.parse_data import make_diff, get_data
from gendiff.format_stylish import stringify
from gendiff.format_plain import make_plain


def parse_cli():
    """Parse command line args and/ or returns tuple filepaths 1, 2 & format.

    :returns: (filepath1, filepath2, format). Tuple of filepath to first_file,
    second_file and format if any, else default."""

    parser = argparse.ArgumentParser(
        prog='gendiff',
        description='Compares two configuration files and shows a difference.'
    )

    parser.add_argument('first_file')
    parser.add_argument('second_file')

    parser.add_argument('-f', '--format', default='stylish',
                        help='set format of output')

    args = parser.parse_args()
    return args.first_file, args.second_file, args.format


def generate_diff(filepath1: str, filepath2: str, format_data='stylish'):
    data1 = get_data(filepath1)
    data2 = get_data(filepath2)
    diff = make_diff(data1, data2)
    if format_data == 'stylish':
        return stringify(diff)
    elif format_data == 'plain':
        return make_plain(diff)


def main():
    first, second, format_data = parse_cli()
    diff = generate_diff(first, second)
    print(diff)


if __name__ == "__main__":
    main()
