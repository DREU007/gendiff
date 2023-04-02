from gendiff.scripts.gendiff import generate_diff
import json


json1_tree_path = 'tests/fixtures/file_tree1.json'
json2_tree_path = 'tests/fixtures/file_tree2.json'
tree_json_result_path = "tests/fixtures/tree_json_result.txt"


def test_tree_json():
    with open(tree_json_result_path, 'r') as result:
        assert generate_diff(json1_tree_path, json2_tree_path) == result.read()


yaml1_tree_path = 'tests/fixtures/file_tree1.yml'
yaml2_tree_path = 'tests/fixtures/file_tree2.yml'
tree_yaml_result_path = "tests/fixtures/tree_yaml_result.txt"


def test_tree_yaml():
    with open(tree_yaml_result_path, 'r') as result:
        assert generate_diff(yaml1_tree_path, yaml2_tree_path) == result.read()


plain_json_result = "tests/fixtures/plain_json_result.txt"


def test_plain_json():
    with open(plain_json_result, 'r') as result:
        assert generate_diff(json1_tree_path, json2_tree_path, "plain"
                             ) == result.read()


json_format_result_path = 'tests/fixtures/json_format_result.json'


def test_json_format():
    with open(json_format_result_path, 'r') as result:
        data = generate_diff(json1_tree_path, json2_tree_path, "json")
        assert json.loads(data) == json.load(result)
