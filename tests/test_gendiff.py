from gendiff.scripts.gendiff import generate_diff


json1_path = 'tests/fixtures/file1.json'
json2_path = 'tests/fixtures/file2.json'

yaml1_path = 'tests/fixtures/file1.yml'
yaml2_path = 'tests/fixtures/file2.yml'

flat_json_result_path = "tests/fixtures/flat_json_result.txt"
flat_yaml_result_path = "tests/fixtures/flat_yaml_result.txt"


def test_flat_json():
    with open(flat_json_result_path, 'r') as flat_json_result:
        assert generate_diff(json1_path, json2_path) == flat_json_result.read()


def test_flat_yaml():
    with open(flat_yaml_result_path, 'r') as flat_yaml_result:
        assert generate_diff(yaml1_path, yaml2_path) == flat_yaml_result.read()
