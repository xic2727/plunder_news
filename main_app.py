from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from source import toutiao, seleitum_toutiao

# 准备不同的任务
tasks = [
    (toutiao.toutiao_list, ("https://www.tushare.pro/news/fenghuang",))
]

# 创建一个线程池，并指定最大线程数
max_threads = 7
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    # 提交任务给线程池，executor.submit 用于提交不同的函数和参数
    futures = [executor.submit(func, *args) for func, args in tasks]

    # 获取任务的执行结果
    for future in as_completed(futures):
        result = future.result()
        print(result)

print("All tasks have finished execution.")
