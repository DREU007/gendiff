import itertools

from gendiff.diff_tree import (
    get_key, get_value, get_children, get_type, TYPE_TO_SYM
)


TRANSLATOR = {True: "true", False: "false", None: "null"}


def translate(value):
    is_bool_or_none = bool(isinstance(value, bool) or value is None)
    return TRANSLATOR.get(value) if is_bool_or_none else value


def deep_line(value, deep_depth, indent=2, replacer=" "):
    if isinstance(value, dict):
        deeper_depth = deep_depth + 2 * indent
        deeper_indent = deeper_depth * replacer
        current_deep_indent = deep_depth * replacer

        deep_lines = [
            f'{deeper_indent}{_key}: '
            f'{deep_line(val, deeper_depth, indent, replacer)}'
            for _key, val in value.items()
        ]

        result = itertools.chain(
            "{", deep_lines, [current_deep_indent + "}"]
        )
        return "\n".join(result)
    return str(translate(value))


def make_stylish(diff_tree, replacer=" ", indent=2):
    def inner(data, depth):
        key = get_key(data)
        type_ = get_type(data)
        values = get_value(data)
        children = get_children(data)

        current_indent = depth * replacer
        deep_depth = depth + indent
        deep_indent = deep_depth * replacer

        symbols = TYPE_TO_SYM.get(type_)

        lines = []
        if values != object:
            for value, sym in zip(values, symbols):
                line = (f"{current_indent}{sym} {key}: "
                        f"{deep_line(value, deep_depth)}")
                lines.append(line)

        else:
            line = f"{current_indent}{symbols} {key}: "
            ends = list(
                map(lambda child: inner(child, deep_depth + indent), children)
            )
            ends = itertools.chain("{", ends, [deep_indent + "}"])

            line += "\n".join(ends)
            lines.append(line)
        return "\n".join(lines)

    root_lines = list(map(
        lambda child: inner(child, depth=2), get_children(diff_tree)
    ))
    root_output = itertools.chain("{", root_lines, "}")
    result = "\n".join(root_output)
    return result
