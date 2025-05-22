from typing import Set, Union
from utils.Coverage import Location


class Seed:
    """Represent an input with additional attributes"""

    _id_counter = 0  # 类变量，用于生成唯一 id

    def __init__(self, data: str, coverage: Set[Location], energy: float = 0.0):
        self.data = data
        self.coverage = coverage
        self.energy = energy
        self.id = self._generate_id(data)

    @staticmethod
    def _generate_id(data: str) -> int:
        """基于数据内容生成唯一ID"""
        return hash(data)
    
    def __getstate__(self):
        """控制序列化内容"""
        return (self.data, self.coverage, self.energy, self.id)

    def __setstate__(self, state):
        """反序列化"""
        self.data, self.coverage, self.energy, self.id = state

    def __str__(self) -> str:
        """Returns data as string representation of the seed"""
        return self.data

    __repr__ = __str__
