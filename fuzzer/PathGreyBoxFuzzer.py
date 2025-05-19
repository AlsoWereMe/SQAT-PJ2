import time
from typing import List, Tuple, Any

from fuzzer.GreyBoxFuzzer import GreyBoxFuzzer
from schedule.PathPowerSchedule import PathPowerSchedule
from runner.FunctionCoverageRunner import FunctionCoverageRunner


class PathGreyBoxFuzzer(GreyBoxFuzzer):
    """Count how often individual paths are exercised."""

    def __init__(self, seeds: List[str], schedule: PathPowerSchedule, is_print: bool):
        super().__init__(seeds, schedule, is_print)
        self.path_set = set()              # 存储所有已发现的路径
        self.last_new_path_time = self.start_time  # 最后发现新路径的时间
        self.total_execs = 0               # 总执行次数

        if is_print:
            print(
                """
┌───────────────────────┬───────────────────────┬───────────────────────┬───────────────────┬───────────────────┬────────────────┬───────────────────┐
│        Run Time       │     Last New Path     │    Last Uniq Crash    │    Total Execs    │    Total Paths    │  Uniq Crashes  │   Covered Lines   │
├───────────────────────┼───────────────────────┼───────────────────────┼───────────────────┼───────────────────┼────────────────┼───────────────────┤"""
            )

    def print_stats(self):
        def format_seconds(seconds):
            hours = int(seconds) // 3600
            minutes = int(seconds % 3600) // 60
            remaining_seconds = int(seconds) % 60
            return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"

        template = """│{runtime}│{path_time}│{crash_time}│{total_exec}│{total_path}│{uniq_crash}│{covered_line}│
├───────────────────────┼───────────────────────┼───────────────────────┼───────────────────┼───────────────────┼────────────────┼───────────────────┤"""
        template = template.format(
            runtime=format_seconds(time.time() - self.start_time).center(23),
            path_time=format_seconds(self.last_new_path_time - self.start_time).center(23),
            crash_time=format_seconds(self.last_crash_time - self.start_time).center(23),
            total_exec=str(self.total_execs).center(19),
            total_path=str(len(self.path_set)).center(19),
            uniq_crash=str(len(set(self.crash_map.values()))).center(16),
            covered_line=str(len(self.covered_line)).center(19),
        )
        print(template)

    def run(self, runner: FunctionCoverageRunner) -> Tuple[Any, str]:
        """Inform scheduler about path frequency"""
        prev_population_len = len(self.population)
        result, outcome = super().run(runner)
        self.total_execs += 1

        if hasattr(runner, "coverage") and callable(getattr(runner, "coverage", None)):
            # 使用 coverage 集合的不可变副本作为路径标识，保证唯一性
            path = frozenset(runner.coverage())
        else:
            # 兜底：用字符串表示
            path = str(getattr(runner, "coverage", lambda: "unknown")())

        # 记录路径
        if path not in self.path_set:
            self.path_set.add(path)
            self.last_new_path_time = time.time()

        # 判断是否有新 seed 加入 population
        if len(self.population) > prev_population_len:
            # 新增了 seed，取最后一个
            seed = self.population[-1]
            self.schedule.update_path_info(seed.id, path)
        else:
            # 没有新 seed，也可以用当前输入构造一个临时 id 反馈
            temp_id = self.inp
            self.schedule.update_path_info(temp_id, path)

        if hasattr(self, "is_print") and self.is_print:
            self.print_stats()

        return result, outcome
