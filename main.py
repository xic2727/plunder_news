from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from plunder_news.source import tushare_fenghaung, tushare_jinrongjie, tushare_10jqka, tushare_sina, tushare_yuncaijing, tushare_eastmoney, tushare_wallstreetcn

# "https://www.tushare.pro/news/jinrongjie",
# "https://www.tushare.pro/news/10jqka",
# "https://www.tushare.pro/news/sina",
# "https://www.tushare.pro/news/yuncaijing",
# "https://www.tushare.pro/news/eastmoney",
# "https://www.tushare.pro/news/wallstreetcn",

# 准备不同的任务
tasks = [
    (tushare_fenghaung.tushare, ("https://www.tushare.pro/news/fenghuang",)),
    (tushare_jinrongjie.tushare, ("https://www.tushare.pro/news/jinrongjie",)),
    (tushare_10jqka.tushare, ("https://www.tushare.pro/news/10jqka",)),
    (tushare_sina.tushare, ("https://www.tushare.pro/news/sina",)),
    (tushare_yuncaijing.tushare, ("https://www.tushare.pro/news/yuncaijing",)),
    (tushare_eastmoney.tushare, ("https://www.tushare.pro/news/eastmoney",)),
    (tushare_wallstreetcn.tushare, ("https://www.tushare.pro/news/wallstreetcn",))
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
