import pytest
from gendiff import generate_diff


@pytest.mark.parametrize(
    argnames="prepared_files",
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
    indirect=True
)
def test_generate_diff(prepared_files):
    file1_path, file2_path, result_render, format_name = prepared_files

    assert result_render == generate_diff(file1_path, file2_path, format_name)
