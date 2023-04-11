import json
import yaml


def get_data(file_path):
    with open(file_path, 'r') as file:
        return file.read(), file_path


def parse_data(data, file_path):
    if file_path.endswith(".yml") or file_path.endswith(".yaml"):
        return yaml.safe_load(data)
    elif file_path.endswith(".json"):
        return json.loads(data)
    else:
        raise NotImplementedError('ERROR: Filetype is not supported yet!')
