import pytest
from utils.Mutator import delete_random_bytes

def test_delete_random_bytes():
    # 测试正常删除
    input_str = "abcdef"
    mutated = delete_random_bytes(input_str)
    assert len(mutated) <= len(input_str), "删除操作后长度应减少"

    # 测试边界条件
    assert delete_random_bytes("") == "", "空输入应返回空"
    assert delete_random_bytes("a") == "a", "单字节输入无法删除"

if __name__ == "__main__":
    pytest.main([__file__])