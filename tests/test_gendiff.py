import os
import json
import pytest
from gendiff import generate_diff


@pytest.mark.parametrize(argnames="prepared_files",
                         argvalues=[
                             (
                                 'tree1.json',
                                 'tree2.json',
                                 "tree_json_result.txt",
                                 "stylish"
                             ),
                             (
                                 'tree1.yml',
                                 'tree2.yml',
                                 "tree_yaml_result.txt",
                                 "stylish"
                             ),
                             (
                                 'tree1.json',
                                 'tree2.json',
                                 "plain_json_result.txt",
                                 "plain"
                             ),
                             (
                                 'tree1.json',
                                 'tree2.json',
                                 "json_format_result.json",
                                 "json"
                             ),
                         ],
                         # indirect=True
                         )
def test_generate_diff(prepared_files):
    before_fp, after_fp, result_fp, _format = prepared_files
    paths = {"before": before_fp, "after": after_fp, "result": result_fp}

    for key, value in paths.items():
        relative_fp = 'fixtures/' + value
        paths[key] = os.path.join(os.path.dirname(__file__), relative_fp)

    with open(paths["result"], 'r') as result:
        if _format != "json":
            assert generate_diff(
                paths["before"], paths["after"], _format) == result.read()
        else:
            data = generate_diff(paths["before"], paths["after"], _format)
            assert json.loads(data) == json.load(result)
