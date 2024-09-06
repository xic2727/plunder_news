import pymongo
import uuid
import json
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 获取环境变量
MONGODB_URI = os.getenv('MONGODB_URI')

# config = json.load(open('../env.json'))


class Mongodb:
    def __init__(self, collection):
        # self.uri = config["MONGODB_URI"]
        self.uri = MONGODB_URI
        self.client = pymongo.MongoClient(self.uri)
        self.db = self.client['news']
        self.collection = collection
        # 选择集合
        self.collection = self.client['news'][self.collection]

    def check_is_exist(self, md5):
        query = {'_id': md5}
        result = self.collection.find_one(query)
        return result

    def insert(self, data):
        # 要插入的文档
        query = {'唯一字段': data['唯一字段']}
        # unique_id = str(uuid.uuid4())
        data['_id'] = data['唯一字段']
        self.collection.insert_one(data)
        print("Record not found, inserting")



if __name__ == '__main__':
    data = {'唯一字段': 'd9548533c3c90ee3765741157b6331a71', '情感分析': '积极',
            '新闻概要': '韩国今年前七个月泡菜进口额创下历史新高，同比增长6.9%，进口量也大幅增加。这可能是由于全球消费者对韩国泡菜的需求增加以及韩国泡菜产业的有效市场推广策略。',
            '新闻行业': '韩国经贸与食品安全行业相关报道', '时间': '2024-09-02 17:54:00.000',
            '所属国家': '韩国', '涉及机构': '韩国关税厅', '涉及人物': '',
            '新闻详情': '1【韩国今年前七个月泡菜进口额创新高】韩国关税厅2日公布的数据显示，今年1月至7月，韩国泡菜进口额同比增加6.9%至9847万美元，创历史新高。数据显示，今年前七个月，韩国泡菜进口额打破2022年同期创下的9649万美元纪录；泡菜进口量同比增加6%，达17.33万余吨，刷新2019年同期最高纪录。',
            '事件影响': '这一增长趋势可能激励韩国泡菜出口企业的生产规模扩大，增加农民种植泡菜的积极性，提高整个韩国泡菜产业的盈利能力。',
            '关键词': '韩国泡菜/进口额创新高/同比增长',
            '事件原因': '可能是由于全球消费者对韩国泡菜的需求增加，以及韩国泡菜产业的创新和市场推广策略有效。',
            '未来预测': '预计未来几个月，韩国泡菜进口额可能会继续保持增长态势，但也需要关注国际市场需求和竞争态势的变化。',
            '消息来源': '官方'}

    mongodb = Mongodb("news_collection")
    result = mongodb.check_is_exist("d9548533c3c90ee3765741157b6331a71")
    print(result)
    # mongodb.insert(data=data)
