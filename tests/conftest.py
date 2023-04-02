import pytest


# @pytest.mark.parametrize("before_fp", "after_fp", "result_fp", [
@pytest.fixture(params=[
    ('tree1.json', 'tree2.json', "tree_json_result.txt", "stylish"),
    ('tree1.yml', 'tree2.yml', "tree_yaml_result.txt", "stylish"),
    ('tree1.json', 'tree2.json', "plain_json_result.txt", "plain"),
    ('tree1.json', 'tree2.json', "json_format_result.json", "json"),
])
def gendiff_fixtures(request):
    return request.param
