from gendiff.scripts.gendiff import generate_diff


filepath1 = 'tests/fixtures/file1.json'
filepath2 = 'tests/fixtures/file2.json'

flat_result_path = "tests/fixtures/flat_json_result.txt"


def test_basic_json():
    with open(flat_result_path, 'r') as flat_result:
        assert generate_diff(filepath1, filepath2) == flat_result.read()
