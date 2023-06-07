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
    data_type = get_type(item)

    if data_type == "root":
        lines = list(map(
            lambda child: make_plain(child), get_children(item)
        ))
        flat_lines = flatten(lines)
        result = filter(None, flat_lines)
        return "\n".join(result)

    key = get_key(item)
    values = get_value(item)
    children = get_children(item)

    if data_type == "parent":
        deep_key = current_key + f"{key}."
        return list(map(
            lambda child: make_plain(child, deep_key), children
        ))

    elif data_type == "same":
        return

    line = f"Property '{current_key + key}'"

    if data_type == "changed":
        val1, val2 = map(value_to_str, values)
        line += f' was updated. From {val1} to {val2}'
        return line

    line += f' was added with value: {value_to_str(values)}' if (
            data_type == "added") else ' was removed'
    return line
