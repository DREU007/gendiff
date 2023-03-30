# import json
from gendiff.parse_data import (
    get_item, get_key, get_values, get_children
)


def make_json(data):
    output = dict()
    for item in get_item(data):
        key = get_key(item)
        # meta = get_meta(item)

        values = get_values(item)
        children = get_children(item)

        if values:
            value = {_key: val for _key, val in item.items() if _key != "key"}
        else:
            value = {_key: val for _key, val in item.items() if _key != "key"
                     if _key != 'children'}
            value["children"] = make_json(children)
        output[key] = value
    return output
