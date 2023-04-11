import json
from gendiff.diff_tree import (
    get_item, get_key, get_values, get_children
)


def prepare_data(data):
    output = dict()
    for item in get_item(data):
        key = get_key(item)

        values = get_values(item)
        children = get_children(item)

        if values:
            value = {_key: val for _key, val in item.items() if _key != "key"}
        else:
            value = {_key: val for _key, val in item.items() if _key != "key"
                     if _key != 'children'}
            value["children"] = prepare_data(children)
        output[key] = value
    return output


def make_json(data):
    result = prepare_data(data)
    return json.dumps(result)
