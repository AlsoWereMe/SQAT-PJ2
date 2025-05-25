import os
import time
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
            + str(self.crashes)
            + ", Start Time: "
            + str(self.start_time)
            + ", End Time: "
            + str(self.end_time)
        )

def run_fuzzing(sample_func, corpus_path, sample_id, schedule_type,run_time):
    
    """运行单个 Sample 的 Fuzzing 测试"""
    # 初始化 Runner 和种子
    f_runner = FunctionCoverageRunner(sample_func)
    seeds = load_object(corpus_path)
    
    if sample_id == 2:
        from utils.Mutator import Sample2Mutator
        from schedule.PathPowerSchedule import Sample2PowerSchedule
        mutator = Sample2Mutator()
        schedule = Sample2PowerSchedule()
        fuzzer = PathGreyBoxFuzzer(
            seeds=seeds,
            schedule=schedule,
            mutator=Sample2Mutator(),
            is_print=True
        )
    else:
        # 选择调度算法
        if schedule_type == "Path":
            fuzzer = PathGreyBoxFuzzer(seeds=seeds, schedule=PathPowerSchedule(), mutator=Mutator(), is_print=True)
        else:
            fuzzer = SeedAwareGreyBoxFuzzer(seeds=seeds, schedule=SeedAwarePowerSchedule(), mutator=Mutator(), is_print=True)
    
    

    # 运行测试
    start_time = time.time()
    fuzzer.runs(f_runner, run_time)  # 运行2小时
    
    # 保存结果
    res = Result(fuzzer.covered_line, set(fuzzer.crash_map.values()), start_time, time.time())
    dump_object(f"_result/Sample-{sample_id}.pkl", res)


    
    

if __name__ == "__main__":
    # 定义测试配置：Sample编号 -> (目标函数, 语料库路径)
    samples = {
        1: (sample1, "corpus/corpus_1", 7200),
        2: (sample2, "corpus/corpus_2", 60),
        3: (sample3, "corpus/corpus_3", 600),
        4: (sample4, "corpus/corpus_4", 600)
    }

    
    # 遍历所有 Sample 和调度算法
    for sample_id, (sample_func, corpus_path, run_time) in samples.items():
        for schedule_type in ["Path"]:  # 两种调度算法
            print(f"Testing Sample {sample_id} with {schedule_type}...")
            run_fuzzing(sample_func, corpus_path, sample_id, schedule_type, run_time)
    
    print("All tests completed. Results saved to _result/ directory.")