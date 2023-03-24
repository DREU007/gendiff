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
    return _obj["key"]


# TODO: missing value if "" - empty string
# TODO: Refactor value if dict()
def get_values(_obj):
    if not (item := _obj.get("value")):
        return None
    if "both" in item:
        return [item["both"]]
    elif "one" in item:
        return [item["one"]]
    else:
        return [item["first"], item["second"]]


def get_meta(_obj):
    return _obj["meta"]


def get_children(_object):
    children = _object.get("children")
    if isinstance(children, dict):
        return [children]  # Return list if single dict
    return children


TRANSLATOR = {True: "true", False: "false", None: "null"}
SPACE = ' '


def stringify(data):
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

        symbols = (first, second) if first else meta.get("condition")

        if values:
            for value, symbol in zip(values, symbols):
                line = f'{indent * SPACE + symbol + " "}{key}: '

                # TODO: Is it possible to remove meta["indent"] and make full
                # recursion??
                def deep_line(current_value, current_indent):
                    if isinstance(current_value, dict):
                        deep_indent = current_indent + 2  # TODO: fix indent +2

                        # TODO: fix (indent + 4)
                        deep_lines = [f'{(current_indent + 4) * SPACE}{_key}'
                                      f': {deep_line(val, deep_indent)}'
                                      for _key, val in current_value.items()]

                        result = itertools.chain(
                            "{", deep_lines,
                            [(current_indent + 2) * SPACE + "}"]  # TODO: fix (indent + 2)
                        )
                        return "\n".join(result)
                    return str(TRANSLATOR.get(current_value, current_value))  # TODO: Apply traslator

                line += deep_line(value, indent)
                lines.append(line)
        elif children:
            line = f'{SPACE * indent + symbols[0] + " "}{key}: '
            line += stringify(children)
            lines.append(line)

    output = itertools.chain("{", lines, [indent * SPACE + "}"])
    return "\n".join(output)
