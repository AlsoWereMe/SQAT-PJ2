import time
from typing import Dict, List, Tuple, Any, Set

from fuzzer.GreyBoxFuzzer import GreyBoxFuzzer
from schedule.SeedAwarePowerSchedule import SeedAwarePowerSchedule
from runner.FunctionCoverageRunner import FunctionCoverageRunner
from utils.Coverage import Location


class SeedAwareGreyBoxFuzzer(GreyBoxFuzzer):
    """跟踪种子年龄和覆盖率变化的增强灰盒模糊测试器"""

    def __init__(
        self, seeds: List[str], schedule: SeedAwarePowerSchedule, is_print: bool
    ):
        # 阻止父类打印表头
        super().__init__(seeds, schedule, is_print=False)

        # 记录每个种子的覆盖变化 {seed.id: coverage_set}
        self.seed_coverage: Dict[str, Set[Location]] = {}
        self.schedule = schedule

        # 自定义打印表头
        if is_print:
            print(
                """
┌───────────────────────┬───────────────────────┬───────────────────────┬───────────────────┬───────────────────┬────────────────┬───────────────────┐
│        Run Time       │    Coverage Growth    │    Last Uniq Crash    │    Total Execs    │    Total Seeds    │  Uniq Crashes  │   Covered Lines   │
├───────────────────────┼───────────────────────┼───────────────────────┼───────────────────┼───────────────────┼────────────────┼───────────────────┤"""
            )

    def run(self, runner: FunctionCoverageRunner) -> Tuple[Any, str]:
        """增强的 run 方法，跟踪覆盖率变化"""
        
        prev_coverage = len(self.covered_line)
        result, outcome = super().run(runner)
        new_coverage = len(self.covered_line)

        # 计算本次覆盖率增长
        coverage_gain = max(0, new_coverage - prev_coverage)

        # 更新当前种子的元信息
        if self.inp in self.population:
            current_seed = next(
                seed for seed in self.population if seed.data == self.inp
            )
            self.schedule.update_seed_metadata(current_seed.id, coverage_gain)

        return result, outcome

    def print_stats(self):
        """自定义统计信息打印"""

        def format_seconds(seconds):
            hours = int(seconds) // 3600
            minutes = int(seconds % 3600) // 60
            remaining_seconds = int(seconds) % 60
            return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"

        current_time = time.time()
        template = """│{runtime}│{coverage_gain}│{crash_time}│{total_exec}│{total_seeds}│{uniq_crash}│{covered_line}│
├───────────────────────┼───────────────────────┼───────────────────────┼───────────────────┼───────────────────┼────────────────┼───────────────────┤"""

        # 计算覆盖率增长率
        total_time_hours = (current_time - self.start_time) / 3600
        coverage_rate = (
            len(self.covered_line) / total_time_hours if total_time_hours > 0 else 0
        )

        template = template.format(
            runtime=format_seconds(current_time - self.start_time).center(23),
            coverage_gain=f"{coverage_rate:.1f}/h".center(23),
            crash_time=format_seconds(self.last_crash_time - self.start_time).center(
                23
            ),
            total_exec=str(self.total_execs).center(19),
            total_seeds=str(len(self.population)).center(19),
            uniq_crash=str(len(set(self.crash_map.values()))).center(16),
            covered_line=str(len(self.covered_line)).center(19),
        )
        print(template)
