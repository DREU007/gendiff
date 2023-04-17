def make_diff(data1, data2):
    # def inner(current_data1, current_data2, ):
    #     all_keys = sorted(
    #         set(current_data1.keys()) | set(current_data2.keys())
    #     )
    #
    #     differences = list()
    #     for key in all_keys:
    #         item = dict()
    #         item["key"] = str(key)
    #
    #         is_key1 = True if key in current_data1 else False
    #         is_key2 = True if key in current_data2 else False
    #
    #         if is_key1 and is_key2:
    #             first = current_data1[key]
    #             second = current_data2[key]
    #
    #             if first == second:
    #                 item["meta"] = {"condition": ' '}
    #                 item["value"] = {"both": first}
    #             else:
    #                 if isinstance(first, dict) and isinstance(second, dict):
    #                     item["meta"] = {"condition": ' '}
    #                     item["children"] = inner(first, second)
    #                 else:
    #                     item["value"] = {"first": first, "second": second}
    #                     item["meta"] = {'first': '-', 'second': '+'}
    #
    #         else:
    #             condition = ('-', current_data1[key]) if is_key1 else (
    #                 '+', current_data2[key]
    #             )
    #
    #             item["value"] = {"one": condition[1]}
    #             item["meta"] = {"condition": condition[0]}
    #
    #         differences.append(item)
    #     return differences
    # return inner(data1, data2)
    return build(data1, data2)


def build_nodes(data1, data2):
    nodes = []
    keys = set(data1.keys()) | set(data2.keys())

    for key in sorted(keys):
        if key not in data1:
            nodes.append({
                "type": "added",
                "key": key,
                "value": data2[key],
            })
        elif key not in data2:
            nodes.append({
                "type": "deleted",
                "key": key,
                "value": data1[key],
            })
        elif data1[key] == data2[key]:
            nodes.append({
                "type": "same",
                "key": key,
                "value": data1[key],
            })
        elif isinstance(data1[key], dict) and isinstance(data2[key], dict):
            nodes.append({
                "type": "parent",  # TODO: is it correct?
                "key": key,
                "children": build_nodes(data1[key], data2[key]),
            })
        else:
            nodes.append({
                "type": "changed",
                "key": key,
                "value": (data1[key], data2[key]),
            })

    return nodes


TYPE_TO_SYM = {"added": "+",
               "deleted": "-",
               "same": " ",
               "parent": " ",
               "changed": ("-", "+")}


def build(data1, data2):
    return {"type": "root", "children": build_nodes(data1, data2)}


def get_item(data):
    # if data["type"] in ("root", "parent"):
    if isinstance(data, list):
        for item in data:
            yield from get_item(item)
    else:
        yield data


def get_key(_obj):
    return _obj["key"]


def get_value(_obj):
    return object if "value" not in _obj else (
        list(val) if isinstance((val := _obj["value"]), tuple) else [val]
    )
    # if "both" in item:
    #     return [item["both"]]
    # elif "one" in item:
    #     return [item["one"]]
    # else:
    #     return [item["first"], item["second"]]


# def get_meta(_obj):
#     return _obj["meta"]
def get_type(_obj):
    return _obj["type"]


def get_children(_object):
    # children = _object.get("children")
    # if isinstance(children, dict):
    #     return [children]  # Return list if single dict
    return _object.get("children")
