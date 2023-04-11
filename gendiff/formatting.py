from gendiff.formats import stringify
from gendiff.formats import make_plain
from gendiff.formats import make_json

FORMAT = {
    "stylish": stringify,
    "plain": make_plain,
    "json": make_json
}


def get_format(diff, format_="stylish"):
    if not (func := FORMAT.get(format_)):
        raise ValueError("ERROR: Wrong format style!")
    return func(diff)
