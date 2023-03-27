import json
import yaml

from gendiff.format_stylish import stringify


def get_json_dict(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def get_yaml_dict(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def get_data(file_path):
    if file_path.endswith(".yml") or file_path.endswith(".yaml"):
        return get_yaml_dict(file_path)
    elif file_path.endswith(".json"):
        return get_json_dict(file_path)
    else:
        raise NotImplementedError('ERROR: Filetype is not supported yet!')


def make_diff(data1, data2):
    indent = 2

    def inner(current_data1, current_data2, depth):
        current_indent = depth + indent
        deep_depth = current_indent + indent

        all_keys = sorted(
            set(current_data1.keys()) | set(current_data2.keys())
        )

        differences = list()
        for key in all_keys:
            item = dict()
            item["key"] = str(key)
            item["meta"] = {"indent": current_indent}  # current_indent

            is_key1 = True if key in current_data1 else False
            is_key2 = True if key in current_data2 else False

            if is_key1 and is_key2:
                first = current_data1[key]
                second = current_data2[key]

                if first == second:
                    item["meta"].update({"condition": ' '})
                    item["value"] = {"both": first}
                else:
                    if isinstance(first, dict) and isinstance(second, dict):
                        item["meta"].update({"condition": ' '})
                        item["children"] = inner(first, second, deep_depth)
                    else:
                        item["value"] = {"first": first, "second": second}
                        item["meta"].update({'first': '-', 'second': '+'})

            else:
                condition = ('-', current_data1[key]) if is_key1 else (
                    '+', current_data2[key]
                )

                item["value"] = {"one": condition[1]}
                item["meta"].update({"condition": condition[0]})

            differences.append(item)
        return differences
    return inner(data1, data2, 0)  # TODO: Fix indent


def generate_diff(filepath1: str, filepath2: str):
    data1 = get_data(filepath1)
    data2 = get_data(filepath2)
    diff = make_diff(data1, data2)
    output = stringify(diff)
    return output


# file_path = '../tests/fixtures/file_tree1.json'
# a = get_json_dict(file_path)
# print(a)