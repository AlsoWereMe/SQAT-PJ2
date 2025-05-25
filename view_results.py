import os
import glob
from utils.ObjectUtils import load_object

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

def print_results():
    # 获取所有结果文件
    result_files = glob.glob("_result/Sample-*.pkl")
    if not result_files:
        print("No results found. Run main.py first.")
        return
    
    # 遍历并打印结果
    for file_path in result_files:
        try:
            res = load_object(file_path)
            filename = os.path.basename(file_path)
            print(f"\n=== {filename} ===")
            print(f"Covered Lines: {len(res.covered_line)}")
            print(f"Unique Crashes: {len(res.crashes)}")
            print(f"Runtime: {res.end_time - res.start_time:.2f} seconds")
        except Exception as e:
            print(f"Error loading {file_path}: {str(e)}")

if __name__ == "__main__":
    print_results()