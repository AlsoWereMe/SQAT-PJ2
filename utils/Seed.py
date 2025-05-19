from typing import Set, Union
from utils.Coverage import Location


class Seed:
    """Represent an input with additional attributes"""

    _id_counter = 0  # 类变量，用于生成唯一 id

    def __init__(self, data: str, _coverage: Set[Location]) -> None:
        """Initialize from seed data"""
        self.data = data
        self.coverage: Set[Location] = _coverage
        self.energy = 0.0

        # 为每个 Seed 分配唯一 id
        self.id = Seed._id_counter
        Seed._id_counter += 1

    def __str__(self) -> str:
        """Returns data as string representation of the seed"""
        return self.data

    __repr__ = __str__
