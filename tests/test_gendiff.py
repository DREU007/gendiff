from gendiff.scripts.gendiff import generate_diff


filepath1 = 'file1.json'
filepath2 = 'file2.json'


def test_basic_json():
    assert generate_diff(filepath1, filepath2) == """{
- follow: false
  host: hexlet.io
- proxy: 123.234.53.22
- timeout: 50
+ timeout: 20
+ verbose: true
}"""
