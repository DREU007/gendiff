import json
import yaml

from gendiff.format_stylish import make_output


JSON_DECODER = {True: 'true',
                False: 'false',
                None: 'null'}

# YAML = {'yml', 'yaml'}


# def get_decoded(data: dict):
#     if isinstance(data, dict):
#         decoded_data = {key: JSON_DECODER.get(val, get_decoded(val)) for key, val in data.items()}
#         print(decoded_data)
#         return decoded_data
#     else:
#         return data


def get_json_dict(file_path):
    with open(file_path, 'r') as file:
        _dict = json.load(file)
        data = _dict
        # data = get_decoded(_dict)
        return data


def get_yaml_dict(file_path):
    with open(file_path, 'r') as file:
        _dict = yaml.safe_load(file)
        # TODO: Fix JSON_DECODER in YAML func
        # data = {key: JSON_DECODER.get(val, val) for key, val in _dict.items()}
        data = _dict
        return data


def get_data(file_path):
    if file_path.endswith(".yml") or file_path.endswith(".yaml"):
        return get_yaml_dict(file_path)
    elif file_path.endswith(".json"):
        return get_json_dict(file_path)
    else:
        raise NotImplementedError('ERROR: Filetype is not supported yet!')


def make_diff(data1, data2):
    indent = 2

    def inner(current_data1, current_data2, current_indent):
        deep_indent = current_indent + indent
        
        all_keys = sorted(
            set(current_data1.keys()) | set(current_data2.keys())
        )

        differences = list()
        for key in all_keys:
            item = dict()
            item["key"] = str(key)
            item["meta"] = {"indent": current_indent}

            first = current_data1.get(key)
            second = current_data2.get(key)

            if first and second:
                item["meta"].update({"condition": ' '})

                if first == second:
                    item["value"] = {"both": first}
                else:
                    if isinstance(first, dict) and isinstance(second, dict):
                        item["children"] = inner(first, second, deep_indent)
                    else:
                        item["value"] = {"first": first, "second": second}
                        item["meta"].update({'first': '-', 'second': '+'})

            else:
                condition = '-' if first else '+'
                only_one = {'-': first, '+': second}
                val = only_one[condition]
                item["value"] = {
                    "one": val if isinstance(val, dict) else str(val)
                }
                item["meta"].update({"condition": condition})

            differences.append(item)

        return differences
    return inner(data1, data2, 2)


def generate_diff(filepath1: str, filepath2: str):
    data1 = get_data(filepath1)
    data2 = get_data(filepath2)
    diff = make_diff(data1, data2)
    output = make_output(diff)
    return output


# file_path = '../tests/fixtures/file_tree1.json'
# a = get_json_dict(file_path)
# print(a)