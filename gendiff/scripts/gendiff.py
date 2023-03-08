#!/usr/bin/env python3
import argparse
import json
import yaml


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


JSON_DECODER = {True: 'true',
                False: 'false',
                None: 'null'}


def get_json_dict(file_path):
    with open(file_path, 'r') as file:
        _dict = json.load(file)
        data = {key: JSON_DECODER.get(val, val) for key, val in _dict.items()}
        return data


def generate_diff(file_path1, file_path2):
    data1 = get_json_dict(file_path1)
    data2 = get_json_dict(file_path2)

    all_keys = sorted(set(data1.keys()) | set(data2.keys()))

    result = '{\n'
    for key in all_keys:
        first = data1.get(key)
        second = data2.get(key)

        first_msg = f'- {key}: {first}\n'
        second_msg = f'+ {key}: {second}\n'

        if first and second:
            if first == second:
                result += f'  {key}: {first}\n'
            else:
                result += first_msg + second_msg
        else:
            result += first_msg if first else second_msg

    result += '}'
    return result


def main():
    first, second, format_data = parse_cli()
    if format_data is None:  # TODO: update None to type of format_data
        print(generate_diff(first, second))


if __name__ == "__main__":
    main()
