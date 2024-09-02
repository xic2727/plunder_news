

class Source(object):
    def __init__(self, url):
        self.url = url

        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": 'session-id=092e43f5-fc6f-4cf3-a205-93b72788fd20; uid=2|1:0|10:1719201613|3:uid|8:Njc0Mzcz|e58b30530dec9f89ffb51421b8b2d25b225c2dc9af8cbae7076b9591e0f446cf; username="2|1:0|10:1719201613|8:username|16:Z3psICoqKiBjb20=|2a38b79775839402c64a54fd025762ed4ecfd69745d55af0fd642d230fd72b6a"',
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }
        self.message = {
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
            "来源网站": "",
            "浏览数": 0,
            "评论数": 0
        }


    def get_news_items(self):
        pass

    def get_llm_return(self):
        pass