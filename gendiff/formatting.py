from gendiff.formats import make_stylish
from gendiff.formats import make_plain
from gendiff.formats import make_json

FORMAT = {
    "stylish": make_stylish,
    "plain": make_plain,
    "json": make_json
}


def formatting(diff, format_="stylish"):
    if not (func := FORMAT.get(format_)):
        raise ValueError("ERROR: Wrong format style!")
    return func(diff)
