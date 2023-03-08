#!/usr/bin/env python3
import json
import yaml
from gendiff.parse_cli import parse_cli


JSON_DECODER = {True: 'true',
                False: 'false',
                None: 'null'}


def get_json_dict(file_path):
    with open(file_path, 'r') as file:
        _dict = json.load(file)
        data = {key: JSON_DECODER.get(val, val) for key, val in _dict.items()}
        return data


def get_yaml_dict(file_path):
    with open(file_path, 'r') as file:
        _dict = yaml.safe_load(file)
        # TODO: Fix JSON_DECODER in YAML func
        data = {key: JSON_DECODER.get(val, val) for key, val in _dict.items()}
        print(_dict)
        return data


def generate_diff(filepath1: str, filepath2: str):
    extension_a = filepath1.rsplit('.', 1)[-1]
    extension_b = filepath2.rsplit('.', 1)[-1]

    # Check type of file
    if extension_a == extension_b == 'json':
        data1 = get_json_dict(filepath1)
        data2 = get_json_dict(filepath2)
    elif extension_a == extension_b == 'yml':
        data1 = get_yaml_dict(filepath1)
        data2 = get_yaml_dict(filepath2)
    else:
        raise TypeError("Error Different FileTypes")

    all_keys = sorted(set(data1.keys()) | set(data2.keys()))

    result = '{\n'
    for key in all_keys:
        first = data1.get(key)
        second = data2.get(key)

        first_msg = f'  - {key}: {first}\n'
        second_msg = f'  + {key}: {second}\n'

        if first and second:
            if first == second:
                result += f'{" " * 4}{key}: {first}\n'
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
