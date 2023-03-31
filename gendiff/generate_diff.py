from gendiff.parse_data import make_diff, get_data
from gendiff.formats import stringify
from gendiff.formats import make_plain
from gendiff.formats import make_json


def generate_diff(filepath1: str, filepath2: str, format_data='stylish'):
    data1 = get_data(filepath1)
    data2 = get_data(filepath2)
    diff = make_diff(data1, data2)
    if format_data == 'stylish':
        return stringify(diff)
    elif format_data == 'plain':
        return make_plain(diff)
    elif format_data == 'json':
        # with open('diff.json', 'w') as file:
        #     diff = make_json(diff)
        #     json.dump(diff, file)
        return make_json(diff)
