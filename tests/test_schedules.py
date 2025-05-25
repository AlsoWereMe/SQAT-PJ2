import pytest
from schedule.PathPowerSchedule import PathPowerSchedule
from utils.Seed import Seed


def test_path_power_schedule():
    schedule = PathPowerSchedule()
    schedule.path_frequency = {"path1": 5, "path2": 1}
    seed = Seed(data="test", _coverage=set())
    schedule.seed_path_map[seed.id] = "path2"
    
    # 调用 assign_energy 时传入单个 Seed
    schedule.assign_energy(seed)  # 现在支持单个 Seed
    assert seed.energy == 10, "低频路径应分配更高能量（10/1=10）"

if __name__ == "__main__":
    pytest.main([__file__])