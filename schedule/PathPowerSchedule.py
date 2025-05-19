from typing import Dict, Sequence
import random

from schedule.PowerSchedule import PowerSchedule
from utils.Seed import Seed


class PathPowerSchedule(PowerSchedule):
    """
    基于路径频率的调度策略：优先选择能触发稀有路径的 seed。
    """

    def __init__(self, seed_num) -> None:
        super().__init__(seed_num)
        self.path_frequency = {}  # 路径频率统计，path(str) -> 频率(int)
        self.seed_path_map = {}   # seed_id(str/int) -> 路径(str)

    def update_path_info(self, seed_id, path):
        """
        更新 seed 与路径的映射关系，并统计路径频率。
        :param seed_id: 种子的唯一标识
        :param path: 本次执行触发的路径(可用字符串或hash表示)
        """
        self.seed_path_map[seed_id] = path  # 记录该 seed 触发的路径
        if path not in self.path_frequency:
            self.path_frequency[path] = 0   # 新路径初始化频率为0
        self.path_frequency[path] += 1      # 路径频率加1

    def choose_seed(self, seeds):
        """
        按路径频率倒数加权采样，优先选择能触发稀有路径的 seed。
        :param seeds: 当前可用的种子列表
        :return: 选中的 seed
        """
        weights = []
        for seed in seeds:
            # 获取该 seed 触发的路径
            path = self.seed_path_map.get(seed.id, None)
            # 获取该路径的频率，默认为1（避免除零）
            freq = self.path_frequency.get(path, 1)
            # 路径频率越低，权重越高
            weights.append(1.0 / freq)
        # 避免所有权重为0的情况，若如此则均匀采样
        if sum(weights) == 0:
            weights = [1.0] * len(seeds)
        return random.choices(seeds, weights=weights, k=1)[0]

    def choose(self, population):
        return self.choose_seed(population)

    def assign_energy(self, population: Sequence[Seed]) -> None:
        """
        为每个 seed 分配能量，能量与路径频率成反比（可用于后续多次变异）。
        :param population: 当前种群（所有种子）
        """
        for seed in population:
            # 获取该 seed 触发的路径
            path = self.seed_path_map.get(seed.id, None)
            # 获取该路径的频率，默认为1
            freq = self.path_frequency.get(path, 1)
            # 能量分配：基础能量为10，频率越低能量越高，最小为1
            seed.energy = max(1, int(10 / freq))

# 在 Fuzzer 执行每个输入后，调用 schedule 的 update_path_info 方法，维护调度信息。
# 在选择 seed 时，调用 schedule 的 choose_seed 方法。