import itertools


def get_item(data):
    if isinstance(data, list):
        for item in data:
            yield from get_item(item)
    else:
        yield data


def get_key(_obj):
    return _obj["key"]


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


def stringify(data, replacer=' ', indent=2):
    def inner(data, depth):
        lines = list()

        deep_depth = depth + indent
        deep_indent = deep_depth * replacer
        current_indent = depth * replacer

        for item in get_item(data):
            key = get_key(item)
            meta = get_meta(item)

            values = get_values(item)
            children = get_children(item)

            first = meta.get("first")
            second = meta.get("second")

            symbols = (first, second) if first else meta.get("condition")
            if values:
                for value, symbol in zip(values, symbols):
                    line = f'{deep_indent + symbol + " "}{key}: '

                    def deep_line(current_value, deep_depth):
                        if isinstance(current_value, dict):
                            deeper_depth = deep_depth + 2 * indent
                            deeper_indent = deeper_depth * replacer
                            current_deep_indent = deep_depth * replacer

                            deep_lines = [
                                f'{deeper_indent}{_key}: '
                                f'{deep_line(val, deeper_depth)}'
                                for _key, val in current_value.items()
                            ]

                            result = itertools.chain(
                                "{", deep_lines, [current_deep_indent + "}"]
                            )
                            return "\n".join(result)
                        return str(TRANSLATOR.get(current_value, current_value))

                    line += deep_line(value, deep_depth + indent)
                    lines.append(line)

            elif children:
                line = f'{deep_indent + symbols[0] + " "}{key}: '
                line += inner(children, deep_depth + indent)
                lines.append(line)

        lines = list(map(lambda _line: _line.rstrip(), lines))
        output = itertools.chain("{", lines, [current_indent + "}"])
        return "\n".join(output)
    return inner(data, 0)
