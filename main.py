import os
import sys
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
    # 参数0、1使用不同算法
    args = sys.argv[1]

    # 构建相应程序的 Runner 对象
    current_sample = sample4
    f_runner = FunctionCoverageRunner(current_sample)

    # 从本地语料库中读取 Seeds 并构建 Fuzzer
    seeds = load_object("corpus/corpus_1")

    if args == 0:
        # 路径调度算法
        grey_fuzzer = PathGreyBoxFuzzer(
            seeds=seeds, schedule=PathPowerSchedule(), is_print=True
        )
    else:
        # 种子年龄调度算法
        grey_fuzzer = SeedAwareGreyBoxFuzzer(
            seeds=seeds, schedule=SeedAwarePowerSchedule(), is_print=True
        )

    # 记录开始时间
    start_time = time.time()

    # 使用 Runner 执行 Fuzzer 中的输入，并指定运行时间(s)
    grey_fuzzer.runs(f_runner, run_time=5)

    # 将 Coverage 与 Crash 的信息导出
    res = Result(
        grey_fuzzer.covered_line,
        set(grey_fuzzer.crash_map.values()),
        start_time,
        time.time(),
    )

    # 自动创建目录
    result_dir = "_result"
    os.makedirs(result_dir, exist_ok=True)

    # 保存信息
    sample_name = f_runner.function.__name__
    # 提取数字部分 "4"
    sample_number = sample_name.replace("sample", "")
    # 生成动态文件名
    result_filename = f"Sample-{sample_number}.pkl"
    result_path = os.path.join("_result", result_filename)
    # 保存结果
    os.makedirs("_result", exist_ok=True)
    dump_object(result_path, res)

    # 查看本次 fuzzing 的执行信息
    print(load_object(result_path))
