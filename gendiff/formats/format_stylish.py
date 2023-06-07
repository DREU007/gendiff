import itertools
from gendiff.diff_tree import get_key, get_value, get_children, get_type


TRANSLATOR = {True: "true", False: "false", None: "null"}
TYPE_TO_SYM = {
    "added": "+",
    "deleted": "-",
    "same": " ",
    "parent": " ",
    "changed": ("-", "+")
}


def translate(value):
    is_bool_or_none = bool(isinstance(value, bool) or value is None)
    return TRANSLATOR.get(value) if is_bool_or_none else value


INDENT = 4


def prepare_indent(depth, sym, replacer=" "):
    return f"{(depth * INDENT - 2) * replacer}{sym} "


def deep_line(value, depth):
    if isinstance(value, dict):
        deep_lines = [
            prepare_indent(depth, " ") + f'{key}: {deep_line(val, depth + 1)}'
            for key, val in value.items()
        ]
        result = "\n".join(deep_lines)
        return f"{{\n{result}\n{prepare_indent(depth - 1, ' ')}}}"

    return str(translate(value))


def make_stylish(diff_tree, depth=0):
    node_type = get_type(diff_tree)
    children = get_children(diff_tree)

    if node_type == "root":
        lines = map(lambda node: make_stylish(node, depth + 1), children)
        lines = "\n".join(lines)
        return f"{{\n{lines}\n}}"

    key = get_key(diff_tree)
    values = get_value(diff_tree)
    symbols = TYPE_TO_SYM.get(node_type)

    if node_type == "parent":
        line = prepare_indent(depth, symbols) + f"{key}: "

        ends = map(lambda node: make_stylish(node, depth + 1), children)
        ends = "\n".join(ends)

        line += f"{{\n{ends}\n" + prepare_indent(depth, ' ') + f"}}"
        return line

    # elif node_type == "same":
    # elif node_type == "changed":
    # elif node_type == "added":
    # elif node_type == "deleted":

    elif node_type in {"same", "changed", "added", "deleted"}:
        lines = []
        for v, sym in zip(values, symbols):
            line = prepare_indent(depth, sym) + f"{key}: {deep_line(v, depth + 1)}"
            lines.append(line)
        return "\n".join(lines)

    else:
        raise ValueError("Unknown node type")

    # return "\n".join(lines)
