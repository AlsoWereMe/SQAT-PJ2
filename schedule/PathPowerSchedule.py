from typing import Dict, Sequence, List,Union
import random
import math
from schedule.PowerSchedule import PowerSchedule
from utils.Seed import Seed


class PathPowerSchedule(PowerSchedule):
    """基于路径频率的调度策略：优先选择能触发稀有路径的 seed。
    
    在 Fuzzer 执行每个输入后，调用 schedule 的 update_path_info 方法，维护调度信息。
    
    在选择 seed 时，调用 schedule 的 choose 方法。
    """

    def __init__(self) -> None:
        super().__init__()
        # 路径频率统计，类型为{path : frequency}
        self.path_frequency = {}

        # 种子路径映射图，类型为{seed_id : path}
        self.seed_path_map = {}

    def assign_energy(self, population: Union[Sequence[Seed], Seed]) -> None:
        """
        支持传入单个 Seed 或 Seed 列表
        """
        if isinstance(population, Seed):
            seeds = [population]  # 将单个 Seed 包装为列表
        else:
            seeds = population
        
        for seed in seeds:
            path = self.seed_path_map.get(seed.id, None)
            freq = self.path_frequency.get(path, 1)
            seed.energy = max(1, int(10 / freq))


    def choose(self, population: List[Seed]):
        """基于能量地加权随机选择"""
        self.assign_energy(population)
        return super().choose(population)

    def update_path_info(self, seed_id, path):
        """
        更新 seed 与路径的映射关系，并统计路径频率。
        :param seed_id: 种子的唯一标识
        :param path: 本次执行触发的路径(可用字符串或hash表示)
        """

        # 记录该 seed 触发的路径
        self.seed_path_map[seed_id] = path

        # 若是新路径初始化频率为0，否则频率加1
        self.path_frequency[path] = self.path_frequency.get(path, 0) + 1
