import pytest
import os
from utils.ObjectUtils import dump_object, load_object

def test_dump_and_load():
    test_data = {"key": "value"}
    dump_object("_result/test.pkl", test_data)
    loaded_data = load_object("_result/test.pkl")
    assert test_data == loaded_data, "持久化数据应与原始数据一致"
    os.remove("_result/test.pkl")  # 清理测试文件

if __name__ == "__main__":
    pytest.main([__file__])