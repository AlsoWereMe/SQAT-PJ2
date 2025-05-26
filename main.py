import os
import sys
import time
from typing import Dict
from fuzzer.PathGreyBoxFuzzer import PathGreyBoxFuzzer
from fuzzer.SeedAwareGryBoxFuzzer import SeedAwareGreyBoxFuzzer
from runner.FunctionCoverageRunner import FunctionCoverageRunner
from schedule.PathPowerSchedule import PathPowerSchedule
from utils.Mutator import Mutator
from schedule.SeedAwarePowerSchedule import SeedAwarePowerSchedule
from samples.Samples import sample1, sample2, sample3, sample4
from utils.ObjectUtils import dump_object, load_object


class Result:
    def __init__(self, coverage, crashes, start_time, end_time):
        self.covered_line = coverage
        self.crashes = crashes
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return (
            "Covered Lines: "
            + str(self.covered_line)
            + ", Crashes Num: "
            + str(len(self.crashes))
            + ", Start Time: "
            + str(self.start_time)
            + ", End Time: "
            + str(self.end_time)
        )


def run_fuzzing(sample_func, corpus_path, sample_id, schedule_type, run_time):
    """运行测试并返回 Result 对象"""
    f_runner = FunctionCoverageRunner(sample_func)
    seeds = load_object(corpus_path)

    if schedule_type == "Path":
        fuzzer = PathGreyBoxFuzzer(
            seeds=seeds,
            schedule=PathPowerSchedule(),
            mutator=Mutator(),
            is_print=True,
        )
    else:
        fuzzer = SeedAwareGreyBoxFuzzer(
            seeds=seeds,
            schedule=SeedAwarePowerSchedule(),
            mutator=Mutator(),
            is_print=True,
        )

    start_time = time.time()
    fuzzer.runs(f_runner, run_time)
    return Result(
        fuzzer.covered_line, set(fuzzer.crash_map.values()), start_time, time.time()
    )


if __name__ == "__main__":
    # 定义所有样本配置
    samples = {
        1: (sample1, "corpus/corpus_1", 60),
        2: (sample2, "corpus/corpus_2", 600),
        3: (sample3, "corpus/corpus_3", 600),
        4: (sample4, "corpus/corpus_4", 1200),
    }

    # 检查命令行参数
    if (
        len(sys.argv) != 2
        or not sys.argv[1].isdigit()
        or int(sys.argv[1]) not in samples
    ):
        print("Usage: python main.py <sample_id>")
        print("Available sample_ids: 1, 2, 3, 4")
        sys.exit(1)

    target_sample_id = int(sys.argv[1])
    target_sample = samples[target_sample_id]

    all_results: Dict[int, Dict[str, Result]] = {}

    # 仅运行目标样本的两种调度算法
    for schedule_type in ["Path", "SeedAware"]:
        print(f"\nTesting Sample {target_sample_id} with {schedule_type}...")
        sample_func, corpus_path, run_time = target_sample
        res = run_fuzzing(
            sample_func, corpus_path, target_sample_id, schedule_type, run_time
        )

        if target_sample_id not in all_results:
            all_results[target_sample_id] = {}
        all_results[target_sample_id][schedule_type] = res

    # 保存并显示结果
    os.makedirs("_result", exist_ok=True)
    for sample_id, schedule_results in all_results.items():
        best_schedule_type, best_result = max(
            schedule_results.items(), key=lambda item: len(item[1].crashes)
        )

        print(f"\n=== Sample {sample_id} 最佳结果 ===")
        print(f"调度算法: {best_schedule_type}")
        print(f"覆盖行数: {len(best_result.covered_line)}")
        print(f"唯一崩溃数量: {len(best_result.crashes)}")
        print(f"运行时间: {best_result.end_time - best_result.start_time:.2f} 秒")

        dump_object(f"_result/Sample-{sample_id}.pkl", best_result)

    print("\n测试完成，结果已保存至 _result/ 目录")
