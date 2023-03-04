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
    print(args.accumulate(args.first_file, args.second_file))


# def preserve_bool(value):
    # return value if value in {'true', 'false', 'null'} else None
# def preserve_bool(val):
#     if val == 'true':
#         return val
#     elif val == 'false':
#         return val
#     else:
#         return None  # Return None to let JSON decoder handle the value.


def generate_diff(file_path1, file_path2):
    data1 = json.load(open(file_path1))
    data2 = json.load(open(file_path2))

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


if __name__ == "__main__":
    parse_cli()
