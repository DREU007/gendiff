from gendiff.diff_tree import (
    get_key, get_value, get_children, get_type, TYPE_TO_SYM
)
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


def make_plain(diff_tree):
    def inner(item, current_key):
        key = get_key(item)
        type_ = get_type(item)
        values = get_value(item)
        children = get_children(item)

        symbol = TYPE_TO_SYM.get(type_)

        if values != object:
            line = f"Property '{current_key + key}'"
            val1 = value_to_str(values[0])

            if len(values) > 1:
                val2 = value_to_str(values[1])
                line += f' was updated. From {val1} to {val2}'
                return line

            elif symbol == " ":
                return

            line += f' was added with value: {val1}' if (
                    symbol == "+") else ' was removed'
            return line

        else:
            deep_key = current_key + f"{key}."
            return list(map(lambda child: inner(child, deep_key), children))

    lines = list(map(lambda child: inner(child, ""), get_children(diff_tree)))
    flat_lines = flatten(lines)
    result = filter(None, flat_lines)
    return "\n".join(result)
