import json
import yaml


JSON_DECODER = {True: 'true',
                False: 'false',
                None: 'null'}

YAML = {'yml', 'yaml'}


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
        return data


def get_data(file_path):
    extension = file_path.rsplit('.', 1)[-1]
    is_yaml = bool(extension in YAML)
    is_json = bool(extension == 'json')
    if is_yaml:
        return get_yaml_dict(file_path)
    elif is_json:
        return get_json_dict(file_path)
    else:
        raise NotImplementedError('ERROR: Filetype is not supported yet!')


def generate_diff(filepath1: str, filepath2: str):
    data1 = get_data(filepath1)
    data2 = get_data(filepath2)
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
