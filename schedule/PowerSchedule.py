import random
from typing import List

from utils.Seed import Seed

MAX_SEEDS = 1000  # 最大种子数量限制


class PowerSchedule:
    """
    能量调度基类，定义了能量分配和种子选择的基本方法。
    """

    def assign_energy(self, population: List[Seed]) -> None:
        """
        为每个种子分配相同的能量，默认实现。
        :param population: 当前所有种子列表
        """
        for seed in population:
            seed.energy = 1

    def normalized_energy(self, population: List[Seed]) -> List[float]:
        """
        归一化能量值，使所有能量之和为1。
        :param population: 当前所有种子列表
        :return: 归一化后的能量列表
        """
        energy = list(map(lambda seed: seed.energy, population))
        sum_energy = sum(energy)  # 所有能量求和
        assert sum_energy != 0    # 防止除零错误
        norm_energy = list(map(lambda nrg: nrg / sum_energy, energy))
        return norm_energy

    def choose(self, population: List[Seed]) -> Seed:
        """
        按归一化能量加权随机选择一个种子。
        :param population: 当前所有种子列表
        :return: 选中的种子
        """
        self.assign_energy(population)
        norm_energy = self.normalized_energy(population)
        # 如果种子数量超过上限，移除能量最小的种子
        if len(population) > MAX_SEEDS:
            min_index = norm_energy.index(min(norm_energy))
            del norm_energy[min_index]
            del population[min_index]
        # 按能量加权随机选择
        seed: Seed = random.choices(population, weights=norm_energy)[0]
        return seed
