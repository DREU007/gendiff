def make_diff(data1, data2):
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
                "type": "parent",
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


def build(data1, data2):
    return {"type": "root", "children": build_nodes(data1, data2)}


def get_item(data):
    if isinstance(data, list):
        for item in data:
            yield from get_item(item)
    else:
        yield data


def get_key(obj):
    return obj["key"]


def get_value(obj):
    return object if "value" not in obj else (
        list(val) if isinstance((val := obj["value"]), tuple) else val
    )


def get_type(obj):
    return obj["type"]


def get_children(obj):
    return obj.get("children")
