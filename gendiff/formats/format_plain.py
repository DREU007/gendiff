from gendiff.diff_tree import (
    get_item, get_key, get_values, get_meta, get_children
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


def make_plain(full_data):
    def inner(data, current_key):
        lines = []
        for item in get_item(data):
            key = get_key(item)
            values = get_values(item)
            children = get_children(item)

            meta = get_meta(item)
            first = meta.get("first")
            second = meta.get("second")

            symbols = (first, second) if first else meta.get("condition")

            if values:
                line = f"Property '{current_key + key}'"
                val1 = value_to_str(values[0])

                if len(values) > 1:
                    val2 = value_to_str(values[1])
                    line += f' was updated. From {val1} to {val2}'
                elif (sym := symbols[0]) == ' ':
                    continue
                else:
                    line += f' was added with value: {val1}' if (
                            sym == "+") else ' was removed'
            else:
                deep_key = current_key + f"{key}."
                line = inner(children, deep_key)
            lines.append(line)
        return "\n".join(lines)

    return inner(full_data, "")
