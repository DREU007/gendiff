import itertools

from gendiff.parse_data import (
    get_item, get_key, get_values, get_meta, get_children
)


TRANSLATOR = {True: "true", False: "false", None: "null"}


def stringify(diff_tree, replacer=' ', indent=2):
    def inner(data, depth):
        lines = list()

        deep_depth = depth + indent
        deep_indent = deep_depth * replacer
        current_indent = depth * replacer

        for item in get_item(data):
            key = get_key(item)

            values = get_values(item)
            children = get_children(item)

            meta = get_meta(item)

            first = meta.get("first")
            second = meta.get("second")

            symbols = (first, second) if first else meta.get("condition")
            if values:
                for value, symbol in zip(values, symbols):
                    line = f'{deep_indent + symbol + " "}{key}: '

                    def deep_line(_value, _deep_depth):
                        if isinstance(_value, dict):
                            deeper_depth = _deep_depth + 2 * indent
                            deeper_indent = deeper_depth * replacer
                            current_deep_indent = _deep_depth * replacer

                            deep_lines = [
                                f'{deeper_indent}{_key}: '
                                f'{deep_line(val, deeper_depth)}'
                                for _key, val in _value.items()
                            ]

                            result = itertools.chain(
                                "{", deep_lines, [current_deep_indent + "}"]
                            )
                            return "\n".join(result)
                        return str(TRANSLATOR.get(_value, _value))

                    line += deep_line(value, deep_depth + indent)
                    lines.append(line)

            elif children:
                line = f'{deep_indent + symbols[0] + " "}{key}: '
                line += inner(children, deep_depth + indent)
                lines.append(line)

        lines = list(map(lambda _line: _line.rstrip(), lines))
        output = itertools.chain("{", lines, [current_indent + "}"])
        return "\n".join(output)
    return inner(diff_tree, 0)
