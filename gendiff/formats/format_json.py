import json
from gendiff.diff_tree import get_key, get_value, get_children


def prepare_data(data):
    output = dict()
    for item in data:
        key = get_key(item)

        values = get_value(item)
        children = get_children(item)

        if values != object:
            value = {k: val for k, val in item.items() if k != "key"}
        else:
            value = {k: val for k, val in item.items() if k != "key"
                     if k != 'children'}
            value["children"] = prepare_data(children)
        output[key] = value
    return output


def make_json(data):
    result = prepare_data(get_children(data))
    return json.dumps(result, indent=4)
