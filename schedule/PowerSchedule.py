import os
import random
from typing import List

from utils.Seed import Seed
from utils.ObjectUtils import load_object, dump_object

MAX_SEEDS = 500  # 最大种子数量限制


class PowerSchedule:
    """
    能量调度基类，定义了能量分配和种子选择的基本方法。
    """
    def __init__(self):
        self.seed_registry: dict[int, str] = self._load_registry()
        self.memory_cache: dict[int, Seed] = {}  # 内存缓存

    def _load_registry(self) -> dict[int, str]:
        """加载种子注册表"""
        try:
            return load_object("corpus/seed_registry.pkl")
        except FileNotFoundError:
            return {}

    def _save_registry(self):
        """保存种子注册表"""
        dump_object("corpus/seed_registry.pkl", self.seed_registry)

    def persist_seed(self, seed: Seed):
        """持久化种子到磁盘"""
        os.makedirs("corpus", exist_ok=True)
        file_path = f"corpus/seed_{seed.id}.pkl"
        
        # 保存种子数据
        dump_object(file_path, seed.data)  # 只保存核心数据
        
        # 更新注册表
        self.seed_registry[seed.id] = {
            "path": file_path,
            "energy": seed.energy,
            "coverage": seed.coverage
        }
        self._save_registry()

        # 从内存缓存移除
        if seed.id in self.memory_cache:
            del self.memory_cache[seed.id]

    def load_seed(self, seed_id: int) -> Seed:
        """按需加载种子到内存"""
        if seed_id in self.memory_cache:
            return self.memory_cache[seed_id]
        
        # 从磁盘加载
        if seed_id in self.seed_registry:
            data = load_object(self.seed_registry[seed_id]["path"])
            metadata = self.seed_registry[seed_id]
            seed = Seed(data, metadata["coverage"])
            seed.energy = metadata["energy"]
            self.memory_cache[seed_id] = seed
            return seed
        return None

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

        # 所有能量求和，并防止除零错误
        sum_energy = sum(energy)
        assert sum_energy != 0
        
        # 能量归一化，map将lambda函数应用到energy每个元素上，并将计算出的值组成迭代器返回，list则将迭代器转为列表返回
        norm_energy = list(map(lambda nrg: nrg / sum_energy, energy))
        return norm_energy

    def choose(self, population: List[Seed]) -> Seed:
        """优化后的选择逻辑"""
        # 内存控制
        while len(population) > MAX_SEEDS:
            # 移除能量最低的种子
            min_energy = min(s.energy for s in population)
            candidates = [s for s in population if s.energy == min_energy]
            seed_to_remove = random.choice(candidates)
            self.persist_seed(seed_to_remove)
            population.remove(seed_to_remove)

        # 按能量选择（自动处理内存/磁盘种子）
        self.assign_energy(population)
        norm_energy = self.normalized_energy(population)
        selected = random.choices(population, weights=norm_energy, k=1)
        return selected[0]  # 返回根据能量权重选择的种子
