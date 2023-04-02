import os
import json
from gendiff import generate_diff


def test_generate_diff(gendiff_fixtures):
    before_fp, after_fp, result_fp, format = gendiff_fixtures
    paths = {"before": before_fp, "after": after_fp, "result": result_fp}

    for key, value in paths.items():
        relative_fp = 'fixtures/' + value
        paths[key] = os.path.join(os.path.dirname(__file__), relative_fp)

    with open(paths["result"], 'r') as result:
        if format != "json":
            assert generate_diff(
                paths["before"], paths["after"], format) == result.read()
        else:
            data = generate_diff(paths["before"], paths["after"], format)
            assert json.loads(data) == json.load(result)
