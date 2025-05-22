import os
import time

from fuzzer.PathGreyBoxFuzzer import PathGreyBoxFuzzer
from fuzzer.SeedAwareGryBoxFuzzer import SeedAwareGreyBoxFuzzer
from runner.FunctionCoverageRunner import FunctionCoverageRunner
from schedule.PathPowerSchedule import PathPowerSchedule
from samples.Samples import sample1, sample2, sample3, sample4
from schedule.SeedAwarePowerSchedule import SeedAwarePowerSchedule
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
            + str(self.crashes)
            + ", Start Time: "
            + str(self.start_time)
            + ", End Time: "
            + str(self.end_time)
        )


if __name__ == "__main__":
    # 构建相应程序的 Runner 对象
    f_runner = FunctionCoverageRunner(sample4)

    # 从本地语料库中读取 Seeds 并构建 Fuzzer
    seeds = load_object("corpus/corpus_1")
    
    # 路径调度算法
    # grey_fuzzer = PathGreyBoxFuzzer(
    #     seeds=seeds, schedule=PathPowerSchedule(), is_print=True
    # )

    # 种子年龄算法
    grey_fuzzer = SeedAwareGreyBoxFuzzer(
        seeds=seeds, schedule=SeedAwarePowerSchedule(), is_print=True 
    )
    
    # 记录开始时间
    start_time = time.time()

    # 使用 Runner 执行 Fuzzer 中的输入，并指定运行时间(s)
    grey_fuzzer.runs(f_runner, run_time=60)

    # 将 Coverage 与 Crash 的信息导出
    res = Result(
        grey_fuzzer.covered_line,
        set(grey_fuzzer.crash_map.values()),
        start_time,
        time.time(),
    )

    # 保存信息
    dump_object("_result" + os.sep + "Sample-1.pkl", res)

    # 查看本次 fuzzing 的执行信息
    print(load_object("_result" + os.sep + "Sample-1.pkl"))
