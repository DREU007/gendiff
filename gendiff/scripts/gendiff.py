#!/usr/bin/env python3
import argparse
import json


def parse_cli():
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


DECODER = {True: 'true',
           False: 'false',
           None: 'null'}


def generate_diff(file_path1, file_path2):
    with open(file_path1, 'r') as file1:
        dict1 = json.load(file1)
        data1 = {key: DECODER.get(val, val) for key, val in dict1.items()}

    with open(file_path2, 'r') as file2:
        dict2 = json.load(file2)
        data2 = {key: DECODER.get(val, val) for key, val in dict2.items()}

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
