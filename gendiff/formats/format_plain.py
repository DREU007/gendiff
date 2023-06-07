from gendiff.diff_tree import get_key, get_value, get_children, get_type
from gendiff.formats.format_stylish import TRANSLATOR


def value_to_str(value):
    is_bool_or_none = bool(isinstance(value, bool) or value is None)
    if isinstance(value, dict):
        output = '[complex value]'
    elif is_bool_or_none:
        output = TRANSLATOR.get(value)
    elif isinstance(value, int):
        output = str(value)
    else:
        output = f"'{value}'"
    return output


def flatten(items):
    result = []
    for item in items:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def make_plain(item, current_key=""):
    node_type = get_type(item)
    children = get_children(item)

    if node_type == "root":
        lines = list(map(
            lambda node: make_plain(node), children
        ))
        flat_lines = flatten(lines)
        result = filter(None, flat_lines)
        return "\n".join(result)

    key = get_key(item)
    values = get_value(item)

    if node_type == "parent":
        deep_key = current_key + f"{key}."
        return list(map(
            lambda node: make_plain(node, deep_key), children
        ))

    elif node_type == "same":
        return

    line = f"Property '{current_key + key}'"

    if node_type == "changed":
        val1, val2 = map(value_to_str, values)
        line += f' was updated. From {val1} to {val2}'
        return line

    elif node_type == "added":
        line += f' was added with value: {value_to_str(values)}'
        return line

    elif node_type == "deleted":
        line += ' was removed'
        return line

    else:
        raise ValueError("Unknown node type")
