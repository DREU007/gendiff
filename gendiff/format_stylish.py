# TODO: Make formatter that return detailed difference
# '-' is removed
# '+' is added
# ' ' is kept the same
import itertools


def get_item(data):
    if isinstance(data, list):
        for item in data:
            yield from get_item(item)
    else:
        yield data


def get_key(_obj):
    return _obj.get("key")


# TODO: missing value if "" - empty string
# TODO: Refactor value if dict()
def get_values(_obj):
    if not (item := _obj.get("value")):
        return None
    if value := item.get("both"):
        return [value]
    elif one := item.get("one"):

        return [one]
    else:
        first = item.get("first")
        second = item.get("second")
        return [first, second] if first and second else (
            [first] if first else [second])


def get_meta(_object):
    return _object.get("meta")


def get_children(_object):
    children = _object.get("children")
    if isinstance(children, dict):
        return [children]  # Return list if single dict
    return children


# def is_simple(data):
#     if isinstance(data, list):
#         return False
#     return True


REPLACER = ' '


def make_output(data):
    lines = list()

    indent = None
    for item in get_item(data):
        key = get_key(item)

        meta = get_meta(item)
        indent = meta["indent"]

        values = get_values(item)
        children = get_children(item)

        first = meta.get("first")
        second = meta.get("second")

        symbols = [first, second] if first and second else (
            [x] if (x := meta.get("condition")) else (
                [first] if first else [second]
            )
        )

        if values:
            for value, symbol in zip(values, symbols):
                line = f'{indent * REPLACER + symbol + " "}{key}: '

                def deep_line(current_value, current_indent):
                    if isinstance(current_value, dict):
                        deep_indent = current_indent + 2
                        _lines = [f'{(current_indent + 4) * REPLACER}{k}: {deep_line(v, deep_indent)}'  # TODO: fix (indent + 4)
                                  for k, v in current_value.items()]
                        result = itertools.chain(
                            "{", _lines, [(current_indent + 2) * REPLACER + "}"]  # TODO: fix (indent + 2)
                        )
                        return "\n".join(result)
                    else:
                        return current_value

                line += deep_line(value, indent)
                lines.append(line)
        elif children:
            line = f'{REPLACER * indent + symbols[0] + " "}{key}: '
            line += make_output(children)
            lines.append(line)

    output = itertools.chain("{", lines, [indent * REPLACER + "}"])
    return "\n".join(output)

#     if not is_simple(data):
#         output += f'{replacer * (indent - indent_step)}{"}"}\n'
#     return output
#
# def stringify(data, replacer=' ', indent=1):
#     if isinstance(data, dict):
#         new_object = make_object(data, replacer=replacer, indent=indent)
#         return generate_output(new_object).strip()
#     return str(data)