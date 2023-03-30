#!/usr/bin/env python3
from gendiff.parse_cli import parse_cli
from gendiff import generate_diff


def main():
    first, second, format_data = parse_cli()
    diff = generate_diff(first, second, format_data)
    print(diff)


if __name__ == "__main__":
    main()
