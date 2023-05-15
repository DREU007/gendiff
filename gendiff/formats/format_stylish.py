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


def prepare_indent(depth, sym, replacer=" "):
    return f"{depth * replacer}{sym} "


INDENT = 2


def deep_line(value, depth):
    if isinstance(value, dict):
        deeper = depth + 2 * INDENT

        deep_lines = [
            prepare_indent(deeper, " ") + f'{key}: {deep_line(val, deeper)}'
            for key, val in value.items()
        ]

        result = itertools.chain(
            "{", deep_lines, [prepare_indent(depth, " ") + "}"]
        )
        return "\n".join(result)
    return str(translate(value))


def make_stylish(diff_tree, depth=0):
    node_type = get_type(diff_tree)
    children = get_children(diff_tree)

    if node_type == "root":
        root_lines = list(
            map(lambda child: make_stylish(child, depth + INDENT), children)
        )

        root_output = itertools.chain("{", root_lines, "}")
        result = "\n".join(root_output)
        return result

    key = get_key(diff_tree)
    symbols = TYPE_TO_SYM.get(node_type)

    lines = []

    if node_type == "parent":
        line = prepare_indent(depth, symbols) + f"{key}: "

        ends = list(map(
            lambda child: make_stylish(child, depth + 2 * INDENT), children
        ))

        ends = itertools.chain(
            "{", ends, [prepare_indent(depth + INDENT, "}").rstrip()]
        )

        line += "\n".join(ends)
        lines.append(line)

    else:
        values = get_value(diff_tree)

        for value, sym in zip(values, symbols):
            line = (
                prepare_indent(depth, sym) + f"{key}: "
                f"{deep_line(value, depth)}"
            )
            lines.append(line)

    return "\n".join(lines)
