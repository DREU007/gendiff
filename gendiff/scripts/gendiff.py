#!/usr/bin/env python3
import argparse
from gendiff.parse_data import generate_diff


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

    parser.add_argument('-f', '--format',
                        help='set format of output')

    args = parser.parse_args()
    # print(args.accumulate(args.first_file, args.second_file))
    return args.first_file, args.second_file, args.format


def main():
    first, second, format_data = parse_cli()
    if format_data is None:  # TODO: update None to type of format_data
        print(generate_diff(first, second))


if __name__ == "__main__":
    main()
