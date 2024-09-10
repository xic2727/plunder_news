from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from source import toutiao
from source import netease

# 准备不同的任务
tasks = [
    toutiao.toutiao_list,
    netease.netease_list,
    netease.netease_hotlist
]

# 创建一个线程池，并指定最大线程数
max_threads = 4
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    # 提交任务给线程池，无需传递参数
    futures = [executor.submit(func) for func in tasks]

    # 获取任务的执行结果
    for future in as_completed(futures):
        try:
            result = future.result()
            print(result)
        except Exception as e:
            print(f"任务执行时发生异常: {e}")

print("All tasks have finished execution.")