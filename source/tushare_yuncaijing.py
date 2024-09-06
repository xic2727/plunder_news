import json
from datetime import datetime, time

import requests
from bs4 import BeautifulSoup

# from openai_api_chatglm import simple_chat
from llm.baidu_qianfan import simple_chat, news_summary
from uitls import post_mongodb
from uitls import tools

message = {
    "唯一字段": "",
    "新闻行业": "",
    "时间": "",
    "所属国家": "",
    "涉及机构": "",
    "涉及人物": "",
    "新闻详情": "",
    "事件影响": "",
    "关键词": "",
    "事件原因": "",
    "未来预测": "",
    "消息来源": "",
    "情感分析": "",
    "来源网站": "云财经",
    "浏览数": 0,
    "评论数": 0
}


def tushare(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": 'session-id=047a6714-6f70-487c-81a0-40a65f152ea4; uid=2|1:0|10:1725586232|3:uid|8:Njc0Mzcz|184be7fd54c4d2f1074c463b879d9ce35b8031686a4b9a8cd4bbdb350ca55451; username="2|1:0|10:1725586232|8:username|16:Z3psICoqKiBjb20=|93af3c5e13838bba0f33c3d9e49e7fc222f20a797b04fe09d7a088eb6c73e7b7"',
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }

    response = requests.request("GET", url, headers=headers)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")

    items = soup.find_all("div", {"class": "none_class news_item"})

    max = 100 if len(items) > 100 else len(items)
    # 获取当前日期
    current_date = datetime.now().date()

    mongodb = post_mongodb.Mongodb()

    for item in items[0:max]:
        # print(
        #     item.find("div", {"class": "news_datetime"}).text,
        #     item.find("div", {"class": "news_content"}).text,
        # )

        news_content = item.find("div", {"class": "news_content"}).text
        news_datetime = item.find("div", {"class": "news_datetime"}).text
        # 将时间字符串转换为 datetime 对象，并附加到当前日期
        news_datetime = datetime.strptime(news_datetime, "%H:%M").replace(year=current_date.year,
                                                                          month=current_date.month,
                                                                          day=current_date.day)
        md5 = tools.calculate_md5(news_content)
        if mongodb.check_is_exist(md5):
            print("数据已存在")
            continue

        try:
            content = simple_chat(
                prompt=news_content, model="ERNIE-Speed-128K", use_stream=False
            )
            print(content)
            content = json.loads(content)

        except Exception as e:
            print(f"ai分析失败:{e}")
            continue

        try:
            global message
            message["唯一字段"] = md5
            message["情感分析"] = content["情感分析"].strip()
            message["新闻概要"] = content["新闻概要"].strip()
            message["新闻行业"] = content["新闻行业"].strip()
            message["时间"] = news_datetime
            message["所属国家"] = content["所属国家"].strip()
            message["涉及机构"] = content["涉及机构"].strip()
            message["涉及人物"] = content["涉及人物"].strip()
            message["新闻详情"] = news_content.strip()
            message["事件影响"] = content["事件影响"].strip()
            message["关键词"] = content["关键词"].strip()
            message["事件原因"] = content["事件原因"].strip()
            message["未来预测"] = content["未来预测"].strip()
            message["消息来源"] = content["消息来源"].strip()
            message["情感分析"] = content["情感分析"].strip()


            print(message)
            mongodb.insert(data=message)

        except:
            print("插入数据库失败")
            continue


if __name__ == "__main__":
    urls = [
        "https://www.tushare.pro/news/fenghuang",
        # "https://www.tushare.pro/news/jinrongjie",
        # "https://www.tushare.pro/news/10jqka",
        # "https://www.tushare.pro/news/sina",
        # "https://www.tushare.pro/news/yuncaijing",
        # "https://www.tushare.pro/news/eastmoney",
        # "https://www.tushare.pro/news/wallstreetcn",
    ]
    for url in urls:
        print(f"开始获取新闻{url}")
        tushare(url)
