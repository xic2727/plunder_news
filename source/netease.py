import json
import sys, os
import re
from datetime import datetime, time
import time


import requests
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from llm.baidu_qianfan import simple_chat, news_summary, simple_chat_app
from uitls import post_mongodb
from uitls import tools



mongodb = post_mongodb.Mongodb("app_collection")

message = {
    "唯一字段": "",
    "新闻标题":"",
    "新闻来源": "",
    "新闻摘要": "",
    "新闻正文": "",
    "新闻评论": "",
    "情感分析": "",
    "新闻行业": "",
    "新闻概要": "",
    "所属国家": "",
    "图片列表": "",

    "涉及机构": "",
    "涉及人物": "",
    "事件影响": "",
    "关键词": "",
    "事件原因": "",
    "未来预测": "",
    "消息来源": "",
    "评论分析": "",

    "来源网站": "网易新闻",
    "评论数": 0,
    "分享数": 0,
    "点赞数": 0,
    "阅读数": 0
}

def remove_html_tags(text):
    clean = re.compile('<.*?>')  # 创建正则表达式匹配HTML标签
    return re.sub(clean, '', text)  # 替换掉HTML标签


def netease_detail(id):
    """
    返回新闻正文、图片列表
    :param id:
    :return:
    """
    url = f"https://gw.m.163.com/nc-omad/api/v1/article/preload/{id}/full"

    payload = {}
    headers = {
        'User-Agent': 'NewsApp/71.1 iOS/17.5.1 (iPhone11,8)',
        'User-U': 'Dr/z3f1T0hVY+2KJVGsDS4HneQ4Vgz8zRIWyqxFlJl4=',
        'User-LC': 'gL29YknF+68qxZc0YBQM7A==',
        'User-C': '5aS05p2h',
        'X-NR-Trace-Id': '1722498159976_12948382704_77D155F0-0FE6-47D9-9529-43C8169AA7F1',
        'User-N': 'WMJEFhR9rRqgr30oX2W7DQ==',
        'X-B3-SpanId': '0',
        'User-id': 'MIh1VDhup4vyHcBoWagNZslHZYsVFs8nj4AFblXgxcPpAdnNipIVNJt+VLiQtQ8ormgi15whFZ9QeayAUoLEZkx0IAprRVp+Jsn69qbj23yAzDRdr4mMRwGkxrjro/HcePBK0dNsyevylzp8V9OOiA==',
        'User-tk': 'S3O8WklP5YU0FqqG/OYh2Ygmpg8plA32jjjvknOnPiVW1K6MID5SNdN3qAta53Kq',
        'User-DA': '0s29TN7+3eTrM8C8wV/0sS/myospKKFNrlDwii9KBnJesXabOlbbSbEXzgUS8XT0',
        'Accept-Language': 'zh-cn',
        'User-D': 'Yyev5RSRLxk09kat+l0Q+A2jzSXi2q77HC5x2oiWASr/+qvZzsNMkMtTU52isZzC',
        'X-B3-Sampled': '1',
        'Cookie': '_ntes_nnid=e47028144b35c62b49a703d71cc11b75,1620649451570; _ntes_nuid=e47028144b35c62b49a703d71cc11b75'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        print(f"{id} 文章获取失败")
        return "", ""
    response = response.json()
    text = response['data'][id]['body']
    clear_text = remove_html_tags(text)

    img = []
    if len(response['data'][id]['img']) is not None:
        for img_url in response['data'][id]['img']:
            img.append(img_url['src'])

    # print(clear_text)
    # print(img)

    return clear_text, img


def netease_comment(id):
    """
    返回评论内容、点赞数、设备、地区
    :return:
    """
    url = f"https://gw.m.163.com/gentie-web/api/v2/products/a2869674571f77b5a0867c3d71db5856/threads/{id}/app/comments/detail?format=building&headLimit=200&ibc=newsappios&cursor=0&limit=10&group=hotlist_A&tailLimit=2&showLevelThreshold=5"

    payload = {}
    headers = {
        'User-Agent': 'NewsApp/71.1 iOS/17.5.1 (iPhone11,8)',
        'User-U': 'Dr/z3f1T0hVY+2KJVGsDS4HneQ4Vgz8zRIWyqxFlJl4=',
        'User-LC': 'gL29YknF+68qxZc0YBQM7A==',
        'User-C': '5aS05p2h',
        'X-NR-Trace-Id': '1722499195772_12908003648_77D155F0-0FE6-47D9-9529-43C8169AA7F1',
        'User-N': 'WMJEFhR9rRqgr30oX2W7DQ==',
        'X-B3-SpanId': '0',
        'User-id': 'MIh1VDhup4vyHcBoWagNZslHZYsVFs8nj4AFblXgxcPpAdnNipIVNJt+VLiQtQ8ormgi15whFZ9QeayAUoLEZkx0IAprRVp+Jsn69qbj23yAzDRdr4mMRwGkxrjro/HcePBK0dNsyevylzp8V9OOiA==',
        'User-tk': 'S3O8WklP5YU0FqqG/OYh2Ygmpg8plA32jjjvknOnPiVW1K6MID5SNdN3qAta53Kq',
        'User-DA': '0s29TN7+3eTrM8C8wV/0sS/myospKKFNrlDwii9KBnJesXabOlbbSbEXzgUS8XT0',
        'Accept-Language': 'zh-cn',
        'User-D': 'Yyev5RSRLxk09kat+l0Q+A2jzSXi2q77HC5x2oiWASr/+qvZzsNMkMtTU52isZzC',
        'X-B3-Sampled': '1',
        'Cookie': '_ntes_nnid=e47028144b35c62b49a703d71cc11b75,1620649451570; _ntes_nuid=e47028144b35c62b49a703d71cc11b75'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    if response['code'] == 1070002:
        print(f"{id} 评论获取失败")
        return "", ""

    comments_list = []
    comments_str = ""
    comments_str_clean = ""

    items = response['data']
    print(f"{id} 评论数：{len(items)}")

    for item in items['comments'].items():
        # print(item)
        comment, digg_count, deviceName, location = item[1]['content'], item[1]['vote'], (item[1]['deviceModelInfo']).get("deviceName", "未知"), item[1]['user']['location']
        comments_list.append((comment, digg_count, deviceName, location))
    sorted_comments = sorted(comments_list, key=lambda x: x[1], reverse=True)

    # 输出排序后的评论
    for comment, digg_count, deviceName, location in sorted_comments:
        comments_str += f"{comment} | {digg_count} | {deviceName} | {location}" + "\n"
        comments_str_clean += f"{comment}" + "\n"

    # print(comments_str)
    return comments_str, comments_str_clean

def netease_list():
    """
    获取新闻列表
    :return:
    """

    message = {
        "唯一字段": "",
        "新闻标题": "",
        "新闻来源": "",
        "新闻摘要": "",
        "新闻正文": "",
        "新闻评论": "",
        "情感分析": "",
        "新闻行业": "",
        "新闻概要": "",
        "所属国家": "",
        "图片列表": "",

        "涉及机构": "",
        "涉及人物": "",
        "事件影响": "",
        "关键词": "",
        "事件原因": "",
        "未来预测": "",
        "消息来源": "",
        "评论分析": "",

        "来源网站": "网易新闻",
        "评论数": 0,
        "分享数": 0,
        "点赞数": 0,
        "阅读数": 0
    }


    url = "https://gw.m.163.com/nc/api/v1/feed/dynamic/headline-list?passport=Dr/z3f1T0hVY+2KJVGsDS4HneQ4Vgz8zRIWyqxFlJl4%3D&devId=Yyev5RSRLxk09kat+l0Q+A2jzSXi2q77HC5x2oiWASr/+qvZzsNMkMtTU52isZzC&version=71.1&spever=false&net=wifi&lat&lon&ts=1722498157&sign=2MzoCzhkSFMRYOE5dRqDL58QycPdcy8AfLDagMumrct48ErR02zJ6/KXOnxX046I&encryption=1&canal=appstore&offset=0&size=25&fn=3&LastStdTime&open&openpath&from=toutiao&prog=LTitleA&refreshCard=dropdown_0"

    payload = {}
    headers = {
        'User-Agent': 'NewsApp/71.1 iOS/17.5.1 (iPhone11,8)',
        'User-U': 'Dr/z3f1T0hVY+2KJVGsDS4HneQ4Vgz8zRIWyqxFlJl4=',
        'User-LC': 'gL29YknF+68qxZc0YBQM7A==',
        'User-C': '5aS05p2h',
        'X-NR-Trace-Id': '1722498157218_12948689200_77D155F0-0FE6-47D9-9529-43C8169AA7F1',
        'User-N': 'WMJEFhR9rRqgr30oX2W7DQ==',
        'X-B3-SpanId': '0',
        'User-id': 'MIh1VDhup4vyHcBoWagNZslHZYsVFs8nj4AFblXgxcPpAdnNipIVNJt+VLiQtQ8ormgi15whFZ9QeayAUoLEZkx0IAprRVp+Jsn69qbj23yAzDRdr4mMRwGkxrjro/HcePBK0dNsyevylzp8V9OOiA==',
        'User-tk': 'S3O8WklP5YU0FqqG/OYh2Ygmpg8plA32jjjvknOnPiVW1K6MID5SNdN3qAta53Kq',
        'User-DA': '0s29TN7+3eTrM8C8wV/0sS/myospKKFNrlDwii9KBnJesXabOlbbSbEXzgUS8XT0',
        'Accept-Language': 'zh-cn',
        'User-D': 'Yyev5RSRLxk09kat+l0Q+A2jzSXi2q77HC5x2oiWASr/+qvZzsNMkMtTU52isZzC',
        'X-B3-Sampled': '1',
        'Cookie': '_ntes_nnid=e47028144b35c62b49a703d71cc11b75,1620649451570; _ntes_nuid=e47028144b35c62b49a703d71cc11b75'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    # print(response)

    items = response['data']['items']
    # print(len(items))

    for item in items[4:]:
        # print(item)
        id = item.get('docid')
        print(id)

        md5 = tools.calculate_md5(item.get('title'))
        if mongodb.check_is_exist(md5):
            print("数据已存在")
            continue

        message["唯一字段"] = tools.calculate_md5(item.get('title'))
        message["新闻标题"] = item.get('title')
        message["新闻来源"] = item.get('source')
        message["发布时间"] = item.get('ptime')
        message["评论数"] = item.get('replyCount')

        message["链接地址"] = f"https://c.m.163.com/news/a/{id}.html"
        message["新闻正文"], message["图片列表"] = netease_detail(id)
        if message["新闻正文"] == "":
            continue
        message["新闻评论"], comments_str_clean = netease_comment(id)
        # print(message)

        try:
            content = simple_chat_app(
                prompt=message["新闻标题"] + message["新闻正文"], comment=comments_str_clean, model="ERNIE-Speed-128K", use_stream=False
            )
            # print(content)
            content = json.loads(content)

        except Exception as e:
            print(f'ai分析失败:{e} \n {message["新闻标题"]} \n {message["新闻正文"]} \n {comments_str_clean}')
            continue

        message['情感分析'] = content.get('情感分析', '')
        message['新闻行业'] = content.get('新闻行业', '')
        message['新闻概要'] = content.get('新闻概要', '')
        message['所属国家'] = content.get('所属国家', '')
        message['涉及机构'] = content.get('涉及机构', '')
        message['涉及人物'] = content.get('涉及人物', '')
        message['事件影响'] = content.get('事件影响', '')
        message['关键词'] = content.get('关键词', '')
        message['事件原因'] = content.get('事件原因', '')
        message['未来预测'] = content.get('未来预测', '')
        message['消息来源'] = content.get('消息来源', '')
        # 评论为0不需要分析
        message['评论分析'] = '' if message["评论数"] == 0 else content.get('评论分析', '')

        print("*" * 100)
        print(message)
        print("*" * 100)

        mongodb.insert(data=message)

def netease_hotlist():
    """
    获取热榜
    :return:
    """

    message = {
        "唯一字段": "",
        "新闻标题": "",
        "新闻来源": "",
        "新闻摘要": "",
        "新闻正文": "",
        "新闻评论": "",
        "情感分析": "",
        "新闻行业": "",
        "新闻概要": "",
        "所属国家": "",
        "图片列表": "",

        "涉及机构": "",
        "涉及人物": "",
        "事件影响": "",
        "关键词": "",
        "事件原因": "",
        "未来预测": "",
        "消息来源": "",
        "评论分析": "",

        "来源网站": "网易新闻",
        "评论数": 0,
        "分享数": 0,
        "点赞数": 0,
        "阅读数": 0
    }

    url = "https://gw.m.163.com/nc/api/v1/feed/dynamic/normal-list?version=71.1&spever=false&net=wifi&lat&lon&ts=1722499702&encryption=1&canal=appstore&offset=0&size=100&fn=1&LastStdTime&open&openpath&from=T1467284926140&dayCount=10"

    payload = {}
    headers = {
        'User-Agent': 'NewsApp/71.1 iOS/17.5.1 (iPhone11,8)',
        'User-U': 'Dr/z3f1T0hVY+2KJVGsDS4HneQ4Vgz8zRIWyqxFlJl4=',
        'User-LC': 'gL29YknF+68qxZc0YBQM7A==',
        'User-C': '6KaB6Ze7',
        'X-NR-Trace-Id': '1722499701766_12907443808_77D155F0-0FE6-47D9-9529-43C8169AA7F1',
        'User-N': 'WMJEFhR9rRqgr30oX2W7DQ==',
        'X-B3-SpanId': '0',
        'User-id': 'MIh1VDhup4vyHcBoWagNZslHZYsVFs8nj4AFblXgxcPpAdnNipIVNJt+VLiQtQ8ormgi15whFZ9QeayAUoLEZkx0IAprRVp+Jsn69qbj23yAzDRdr4mMRwGkxrjro/HcePBK0dNsyevylzp8V9OOiA==',
        'User-tk': 'S3O8WklP5YU0FqqG/OYh2Ygmpg8plA32jjjvknOnPiVW1K6MID5SNdN3qAta53Kq',
        'User-DA': '0s29TN7+3eTrM8C8wV/0sS/myospKKFNrlDwii9KBnJesXabOlbbSbEXzgUS8XT0',
        'Accept-Language': 'zh-cn',
        'User-D': 'Yyev5RSRLxk09kat+l0Q+A2jzSXi2q77HC5x2oiWASr/+qvZzsNMkMtTU52isZzC',
        'X-B3-Sampled': '1',
        'Cookie': '_ntes_nnid=e47028144b35c62b49a703d71cc11b75,1620649451570; _ntes_nuid=e47028144b35c62b49a703d71cc11b75'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    # print(response)

    items = response['data']['items']
    print(len(items))
    for item in items[4:]:
        # print(item)
        id = item.get('postid')
        print(id)

        md5 = tools.calculate_md5(item.get('title'))
        if mongodb.check_is_exist(md5):
            print("数据已存在")
            continue

        message["新闻标题"] = item.get('title')
        message["新闻来源"] = item.get('source')
        message['新闻摘要'] = item.get('aheadBody')
        message["发布时间"] = item.get('ptime')
        message["评论数"] = item.get('replyCount')
        message["链接地址"] = f"https://c.m.163.com/news/a/{id}.html"
        message["新闻正文"], message["图片列表"] = netease_detail(id)
        if message["新闻正文"] == "":
            continue

        message["新闻评论"], comments_str_clean = netease_comment(id)
        message["点赞数"] = item.get('votecount')
        message["评论数"] = item.get('replyCount')

        try:
            content = simple_chat_app(
                prompt=message["新闻标题"] + message["新闻正文"], comment=comments_str_clean, model="ERNIE-Speed-128K", use_stream=False
            )
            # print(content)
            content = json.loads(content)

        except Exception as e:
            print(f'ai分析失败:{e} \n {message["新闻标题"]} \n {message["新闻正文"]} \n {comments_str_clean}')
            continue

        message['情感分析'] = content.get('情感分析', '')
        message['新闻行业'] = content.get('新闻行业', '')
        message['新闻概要'] = content.get('新闻概要', '')
        message['所属国家'] = content.get('所属国家', '')
        message['涉及机构'] = content.get('涉及机构', '')
        message['涉及人物'] = content.get('涉及人物', '')
        message['事件影响'] = content.get('事件影响', '')
        message['关键词'] = content.get('关键词', '')
        message['事件原因'] = content.get('事件原因', '')
        message['未来预测'] = content.get('未来预测', '')
        message['消息来源'] = content.get('消息来源', '')
        # 评论为0不需要分析
        message['评论分析'] = '' if message["评论数"] == 0 else content.get('评论分析', '')

        print("*" * 100)
        print(message)
        print("*" * 100)

        mongodb.insert(data=message)




def main():
    """
    组装
    :return:
    """
    pass


if __name__ == '__main__':
    # netease_list()
    netease_hotlist()
    # id = "JBD7S3MJ0001899O"
    # id = "JBI4E6BH0514R9P4"
    # netease_detail(id)
    # netease_comment(id)

    # netease_detail("VCANEHOQ6")