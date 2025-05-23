from typing import Dict, List, Sequence, Tuple
import random
import time

from schedule.PowerSchedule import PowerSchedule
from utils.Seed import Seed


class SeedAwarePowerSchedule(PowerSchedule):
    """基于种子年龄和覆盖增长率的调度策略：
    1. 优先选择年龄较小的种子（最近新增的种子）
    2. 对覆盖率增长贡献大的种子分配更多能量
    """

    def __init__(self) -> None:
        super().__init__()
        # 记录种子的元信息：{seed.id: (创建时间戳, 覆盖增长率)}
        self.seed_metadata: Dict[str, Tuple[float, float]] = {}

    def assign_energy(self, population: Sequence[Seed]) -> None:
        """动态计算能量分配"""
        current_time = time.time()

        for seed in population:
            # 获取种子元信息
            default_meta: Tuple[float, float] = (current_time, 0.0)
            create_time, coverage_gain = self.seed_metadata.get(seed.id, default_meta)

            # 计算年龄因子（单位：小时）
            age = max(1.0, (current_time - create_time) / 3600)  # 防止除零

            # 能量计算 = 基础能量 * 覆盖增长率 / 年龄
            base_energy = 10.0
            seed.energy = max(1, int(base_energy * (coverage_gain + 0.1) / age))

    def choose(self, population: List[Seed]) -> Seed:
        """基于能量地加权随机选择"""
        self.assign_energy(population)
        return super().choose(population)

    def update_seed_metadata(self, seed_id: str, coverage_gain: float):
        """更新种子覆盖增长率和时间戳"""
        current_time = time.time()
        # 保留旧创建时间，只更新覆盖增长率
        old_create_time, _ = self.seed_metadata.get(seed_id, (current_time, 0.0))
        self.seed_metadata[seed_id] = (old_create_time, coverage_gain)
