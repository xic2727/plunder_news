import json
import sys, os
from datetime import datetime, time
import time


import requests
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from llm.baidu_qianfan import simple_chat, news_summary, simple_chat_app
from uitls import post_mongodb
from uitls import tools

from seleitum_toutiao import seleitum_page

# 全局浏览器实例
browser = None


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

    "来源网站": "今日头条",
    "评论数": 0,
    "分享数": 0,
    "点赞数": 0,
    "阅读数": 0
}


def toutiao_detail(id):
    detail, img_src = seleitum_page(id)

    return detail, img_src


def toutiao_comment(id, count=20):
    import requests

    url = f"https://api5-normal-hl.toutiaoapi.com/article/v4/tab_comments/?fold=1&offset=0&group_id={id}&count=200&comment_request_from=1&category=__all__&device_platform=android&os=android&ssmix=a&_rticket=1721696870526&cdid=451db13b-f221-4735-96aa-76c4bfa5259e&channel=update_verify&aid=13&app_name=news_article&version_code=897&version_name=8.9.7&manifest_version_code=8970&update_version_code=89761&ab_version=660830%2C9534796%2C9550917%2C3795191%2C3928650%2C4113875%2C4522573%2C4714450%2C4890008%2C5361614%2C5452730%2C6034695%2C6461459%2C6571806%2C6760620%2C6868072%2C6959547%2C6961665%2C7028329%2C7204586%2C7237725%2C7354842%2C7551466%2C7659315%2C7670553%2C7673026%2C7681476%2C7682659%2C7995293%2C8087084%2C8160327%2C8186512%2C8247503%2C8426871%2C8512477%2C8553210%2C8611793%2C8639938%2C8663350%2C8675077%2C8721364%2C8760183%2C8779951%2C8885971%2C8944447%2C8945471%2C8985781%2C9023661%2C9023668%2C9023689%2C9028094%2C9034362%2C9044858%2C9067502%2C9133018%2C9183639%2C9200775%2C9206929%2C9262164%2C9295447%2C9311413%2C9327892%2C9333000%2C9390085%2C9403358%2C9408359%2C9411959%2C9419063%2C9420136%2C9436478%2C9438609%2C9448256%2C9488616%2C9491690%2C9498830%2C9504208%2C9507197%2C9515255%2C9515258%2C9521265%2C9522148%2C9525601%2C9531290%2C9539780%2C9542578%2C9548040%2C9552747%2C9556333%2C9556447%2C9560959%2C9562655%2C9566552%2C9567211%2C9568458%2C9568608%2C9569018%2C9570274%2C9571118%2C9572269%2C9573897%2C9575692%2C9581579%2C9588022%2C9593750%2C9593902%2C9595682%2C9596361%2C9596953%2C9600315%2C9604025%2C9607837%2C9607949%2C9611577%2C9094555%2C9456251%2C1859936%2C668775%2C4075545%2C9438749%2C9439891%2C9472431%2C9496239%2C9534809%2C9553435%2C9571125%2C668779%2C9534802%2C668776%2C9534811%2C668774%2C8974408%2C9534795%2C9545402%2C662176%2C9534794%2C662099%2C9534762%2C9434049%2C9554871%2C9352450%2C9551788%2C9105000%2C8173403%2C9325339%2C9331598%2C9384146%2C9470952%2C9498604%2C9541903%2C9594021%2C9263629%2C7142413%2C8504306%2C9597943&ab_feature=94563%2C102749&resolution=1080*2276&dpi=440&device_type=21091116C&device_brand=Redmi&language=zh&os_api=30&os_version=11&ac=wifi&dq_param=2&plugin=0&client_vid=3194525%2C2827920&isTTWebView=0&session_id=cca1a646-772f-475d-8067-c9279ecb9917&host_abi=arm64-v8a&tma_jssdk_version=2.53.0&rom_version=miui_v125_v12.5.18.0.rktcnxm&immerse_pool_type=101&iid=2142277281260740&device_id=1130711884249992&openudid=5b7c82c33468d936&oaid=a0089862c45ed726"

    payload = {}
    headers = {
        'Host': 'api5-normal-hl.toutiaoapi.com',
        'Cookie': 'PIXIEL_RATIO=2.75; FRM=new; d_ticket=325d87a321c825261d2a4244062616f4e2aee; uid_tt=73fff7122d245cc6f5edfdafccfbe0c1; uid_tt_ss=73fff7122d245cc6f5edfdafccfbe0c1; sid_tt=bb24b2110c17d07a551881b6326b7262; sessionid=bb24b2110c17d07a551881b6326b7262; sessionid_ss=bb24b2110c17d07a551881b6326b7262; install_id=2142277281260740; ttreq=1$2499aa685121a8b2ce4da0ea65d26deec4496718; store-region=cn-gd; passport_csrf_token=e7d868396996eeb31ce629c63cbb5b9a; passport_csrf_token_default=e7d868396996eeb31ce629c63cbb5b9a; store-region-src=uid; oauth-hash=41747; ttwid=1%7CaB-ysRFHk1h0ZC27Y-kh7t7qyU5Z-U5_4KUSYA05u3o%7C1692769546%7Cee96641163361a6b67afcb1ec2746a8cf97d2f721074fdd9da8c74845993da62; WIN_WH=393_857; odin_tt=c6568f868c4b8741ba344d30b5a80bbd59c5bf2931f2c0ad10c54ed280df37b837edc0ac2f74e781839f6c2b6c017007; tt_webid=1%7CaB-ysRFHk1h0ZC27Y-kh7t7qyU5Z-U5_4KUSYA05u3o%7C1692769546%7Cee96641163361a6b67afcb1ec2746a8cf97d2f721074fdd9da8c74845993da62; sid_guard=bb24b2110c17d07a551881b6326b7262%7C1721398138%7C5184000%7CTue%2C+17-Sep-2024+14%3A08%3A58+GMT',
        'x-ss-req-ticket': '1721696870529',
        'x-tt-dt': 'AAAZHNMXBHFTKENPY7WTPNY6IP2AJILRWWNENBHDHFBJBCD3ARMROBJEGCMNXMWKGASLKGIGJ7WHYGAT5JKJNJKNHC2FCOT5XNMDUQ2565AO3BDOPG2UZMRKJFNJ6LYAH7BUSOZJBC6DDOM4HGBYYGQ',
        'x-tt-trace-log': '02',
        'sdk-version': '2',
        'x-tt-token': '00bb24b2110c17d07a551881b6326b726203f86397176630d177463a9b297caa3877e2b94f4f271cc427a0c09f78cd9118dfd9cb76d55cfb073d30f99b6750078553638c43478d8e2d0ba27b2b29605d4259693677a11450221d70a85ab8eef28c826-1.0.1',
        'passport-sdk-version': '30858',
        'x-vc-bdturing-sdk-version': '2.2.1.cn',
        'x-tt-store-region': 'cn-gd',
        'x-tt-store-region-src': 'did',
        'x-tt-request-tag': 's=-1;p=0',
        'x-ss-dp': '13',
        'x-tt-trace-id': '00-dd2162180d4046060343b88592fd000d-dd2162180d404606-01',
        'user-agent': 'com.ss.android.article.news/8970 (Linux; U; Android 11; zh_CN; 21091116C; Build/RP1A.200720.011; Cronet/TTNetVersion:68deaea9 2022-07-19 QuicVersion:12a1d5c5 2022-06-27)',
        'x-argus': 'Mvl/BP82GGHFMfftHuYAd9OnLlz4iTifvweUCWaplmSxzcFfdtpy8FTAtimstGqodBeoFQmYMdtHd7/NEuBpsNl6+87gqWopuKVY3gTW1sWF6cuwRXGWIkdXtBKlzOq4g7yVgOwyG5a29lzyLCfy31dtN7NzRFqTfK/bE1Vwyl17PhOy6KQUSNb8fJ0XRumi1iXXAgBCFR9iQRtoW5KpkXFXRAsNGGTaunI/C51bae8B7ekAbJJzon7gU9fNUkt1oyoRQb0nCeMUcPwkeDjBu57v',
        'x-gorgon': '8404205300007c4bf83deecc797052ded9b73a20f5ab174f8c41',
        'x-khronos': '1721696870',
        'x-ladon': 'TA49c/BzFMtkL0zZbpnQdt/vQSj7FZKEIxurhTQRmdA18ZT9'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    comments_list = []
    comments_str = ""

    items = response['data']
    for item in items:
        comments, digg_count = item['comment']['text'], item['comment']['digg_count']
        comments_list.append((comments, digg_count))
    sorted_comments = sorted(comments_list, key=lambda x: x[1], reverse=True)

    # 输出排序后的评论
    for comment, likes in sorted_comments[0:count]:
        comments_str += f"{comment} | {likes}" + "\n"

    return comments_str

def toutiao_list():
    import requests

    url = "https://api3-normal-hl.toutiaoapi.com/api/news/feed/v88/?st_time=4572&crypto_info=dGMFEAAAT%2B8cnVLiGMuG660478pw4dmX6UM9H%2B4uzcwX8Rt1yWpeNmxTcYax7M9YvvmUtQI2gQ2t%0AJS6VTTmdMYjM%2Fn368c7tcOZvBaaBjVhvw2DipGZp237unhuYYgMAKfjYSueCmxvMAr72WzBGLAMz%0Am3FGc8LxL5NBMJY%2B5aa5oihRPMk%3D%0A&list_count=17&concern_id=6286225228934679042&refer=1&refresh_reason=1&session_refresh_idx=3&count=20&min_behot_time=1721642977&last_refresh_sub_entrance_interval=1721642992&last_ad_show_interval=13&cached_item_num=0&last_response_extra=%7B%22data%22%3A%22eyJoYXNfZm9sbG93aW5nIjpmYWxzZX0%22%7D&ad_ui_style=%7B%22is_crowd_generalization_style%22%3A2%2C%22van_package%22%3A11000060%7D&lynx_template_data=%5B%5D&lynx_version=2.5.5-rc.1.1-bugfix&tt_from=pull&client_extra_params=%7B%22last_ad_position%22%3A-1%2C%22font_size%22%3A4%2C%22har_state%22%3A0%2C%22hand_state%22%3A1%2C%22cold_session_feed_refresh_cnt%22%3A3%2C%22playparam%22%3A%22codec_type%3A7%2Ccdn_type%3A1%2Cresolution%3A1080*2400%2Cttm_version%3A896000%2Cenable_dash%3A0%2Cunwatermark%3A1%2Cv1_fitter_info%3A1%2Ctt_net_energy%3A4%2Cis_order_flow%3A-1%2Ctt_device_score%3A8.1%2Ctt_enable_adaptive%3A2%22%2C%22recommend_enable%22%3A1%2C%22immerse_pool_type%22%3A101%2C%22immerse_candidate_version%22%3A0%2C%22forbid_loc_rec%22%3A2%2C%22forbid_search_history_rec%22%3A0%2C%22forbid_follow_user_rec%22%3A0%2C%22content_diversity_freq%22%3A0%2C%22ad_download%22%3A%7B%22su%22%3A4600%2C%22pure_mode%22%3A4%7D%2C%22catower_net_quality%22%3A2%2C%22catower_device_overall_performance%22%3A0%7D&device_platform=android&os=android&ssmix=a&_rticket=1721642992956&cdid=451db13b-f221-4735-96aa-76c4bfa5259e&channel=update_verify&aid=13&app_name=news_article&version_code=897&version_name=8.9.7&manifest_version_code=8970&update_version_code=89761&ab_version=668776%2C9534811%2C668774%2C8974408%2C9534795%2C9545402%2C668779%2C9534802%2C660830%2C9534796%2C9550917%2C3795191%2C3928650%2C4113875%2C4522573%2C4714450%2C4890008%2C5361614%2C5452730%2C6034695%2C6461459%2C6571806%2C6760620%2C6868072%2C6959547%2C6961665%2C7028329%2C7204586%2C7237725%2C7354842%2C7551466%2C7659315%2C7670553%2C7673026%2C7681476%2C7682659%2C7995293%2C8087084%2C8160327%2C8186512%2C8247503%2C8426871%2C8512477%2C8522462%2C8553210%2C8611793%2C8639938%2C8663350%2C8675077%2C8721364%2C8760183%2C8779951%2C8885971%2C8944447%2C8945471%2C8985781%2C9023661%2C9023668%2C9023689%2C9028094%2C9034362%2C9044858%2C9067502%2C9133018%2C9183639%2C9200775%2C9206929%2C9262164%2C9295447%2C9311413%2C9327892%2C9333000%2C9390085%2C9403358%2C9408359%2C9411959%2C9419063%2C9420136%2C9436478%2C9438609%2C9448256%2C9488616%2C9491690%2C9498830%2C9504208%2C9507197%2C9515255%2C9515258%2C9521265%2C9522148%2C9525601%2C9531290%2C9539780%2C9542578%2C9548040%2C9552747%2C9556333%2C9556447%2C9560959%2C9562655%2C9566552%2C9567211%2C9568458%2C9568608%2C9569018%2C9570274%2C9571118%2C9572269%2C9573897%2C9575692%2C9581579%2C9588022%2C9593750%2C9593902%2C9595682%2C9596361%2C9596953%2C9600315%2C9604025%2C9607837%2C9607949%2C9094555%2C9456251%2C1859936%2C668775%2C4075545%2C9438749%2C9439891%2C9472431%2C9496239%2C9534809%2C9553435%2C9571125%2C662176%2C9534794%2C662099%2C9534762%2C9434049%2C9554871%2C9352450%2C9551788%2C9105000%2C8173403%2C9325339%2C9331598%2C9384146%2C9470952%2C9498604%2C9541903%2C9594021%2C9263629%2C6231311%2C7142413%2C8504306%2C9597943&ab_feature=94563%2C102749&resolution=1080*2276&dpi=440&device_type=21091116C&device_brand=Redmi&language=zh&os_api=30&os_version=11&ac=wifi&dq_param=2&plugin=0&client_vid=3194525%2C2827920&isTTWebView=0&session_id=76abba83-936c-4ea7-8115-27fd73d96a2e&host_abi=arm64-v8a&tma_jssdk_version=2.53.0&rom_version=miui_v125_v12.5.18.0.rktcnxm&immerse_pool_type=101&iid=2142277281260740&device_id=1130711884249992&openudid=5b7c82c33468d936&oaid=a0089862c45ed726&cmwz=%2526-%2522%2523ws2K45%25407%2524x%257Bx%257B%2B%25210%252434C%255CEFQH7*3%252FMfOk%253B%253CEGGFCuGIzzNJO%253CG%253E-%252F%2525%252F7%2527-%2529G%2560I%255D%252Ca%252Fd_m%253E%253FADGtJEI63&cp=646491e82bff0q1"

    payload = {}
    headers = {
        'Host': 'api3-normal-hl.toutiaoapi.com',
        'Cookie': 'PIXIEL_RATIO=2.75; FRM=new; d_ticket=325d87a321c825261d2a4244062616f4e2aee; uid_tt=73fff7122d245cc6f5edfdafccfbe0c1; uid_tt_ss=73fff7122d245cc6f5edfdafccfbe0c1; sid_tt=bb24b2110c17d07a551881b6326b7262; sessionid=bb24b2110c17d07a551881b6326b7262; sessionid_ss=bb24b2110c17d07a551881b6326b7262; install_id=2142277281260740; ttreq=1$2499aa685121a8b2ce4da0ea65d26deec4496718; store-region=cn-gd; passport_csrf_token=e7d868396996eeb31ce629c63cbb5b9a; passport_csrf_token_default=e7d868396996eeb31ce629c63cbb5b9a; store-region-src=uid; oauth-hash=41747; ttwid=1%7CaB-ysRFHk1h0ZC27Y-kh7t7qyU5Z-U5_4KUSYA05u3o%7C1692769546%7Cee96641163361a6b67afcb1ec2746a8cf97d2f721074fdd9da8c74845993da62; WIN_WH=393_857; odin_tt=c6568f868c4b8741ba344d30b5a80bbd59c5bf2931f2c0ad10c54ed280df37b837edc0ac2f74e781839f6c2b6c017007; tt_webid=1%7CaB-ysRFHk1h0ZC27Y-kh7t7qyU5Z-U5_4KUSYA05u3o%7C1692769546%7Cee96641163361a6b67afcb1ec2746a8cf97d2f721074fdd9da8c74845993da62; sid_guard=bb24b2110c17d07a551881b6326b7262%7C1721398138%7C5184000%7CTue%2C+17-Sep-2024+14%3A08%3A58+GMT',
        'x-ss-req-ticket': '1721642992960',
        'x-tt-dt': 'AAARAMLA6HCTOKLM47BRW74524QCE4O64B6WJ7UR43537Y6FFI47GZXTFKDOMS7ONAA3ZR6X6NLPPPGTXAVXDO4P2BF53KHJMZDKM2JG2ZZQW7HSSMX4OKRVABNASRQTBGNZN52TLQCUUYMGSHFLQII',
        'x-tt-trace-log': '02',
        'sdk-version': '2',
        'x-tt-token': '00bb24b2110c17d07a551881b6326b726203f86397176630d177463a9b297caa3877e2b94f4f271cc427a0c09f78cd9118dfd9cb76d55cfb073d30f99b6750078553638c43478d8e2d0ba27b2b29605d4259693677a11450221d70a85ab8eef28c826-1.0.1',
        'passport-sdk-version': '30858',
        'x-vc-bdturing-sdk-version': '2.2.1.cn',
        'x-tt-store-region': 'cn-gd',
        'x-tt-store-region-src': 'did',
        'x-tt-request-tag': 's=-1;p=0',
        'x-ss-dp': '13',
        'x-tt-trace-id': '00-d9eb46de0d4046060343b8871904000d-d9eb46de0d404606-01',
        'user-agent': 'com.ss.android.article.news/8970 (Linux; U; Android 11; zh_CN; 21091116C; Build/RP1A.200720.011; Cronet/TTNetVersion:68deaea9 2022-07-19 QuicVersion:12a1d5c5 2022-06-27)',
        'x-argus': 'ChsvJwrhsVz2W+SoYF8JnYv12r3IyOaoYQ9+pSpbrCjjtNJW8zguvNRMqtTv5s3yJZJNMehpubo+1o60RS4SnJVgYF8UUHtfOrJ5ghBc5brh1h78XD6bWspYb7Ll0x02cidcDpjQBOp/tpLs+OClQ4cSvG1XczP0jqyaSE7M7Wf8oZnOmH49b6iF6UvhR1cnS+Rl8m7Vaa7mxyF1ayc6vRs3oqlefgDr3NTpOt65s8bOmJKd/dUSuWcSfvQI8JXbZXMN3JjyP/z57v2rGR5QMlZo',
        'x-gorgon': '840400b80000380fe6adf79d6f3da67a07963645b1d991cf6e4d',
        'x-khronos': '1721642992',
        'x-ladon': 'hvmkfeP/usytFbe4+VMwRdcrLI5Gh6G1YBgbF9CtoKwqYrmh'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    # print(response)

    items = response['data']

    for item in items[4:]:
        item = json.loads(item['content'])
        # 没有消息id跳过
        if item.get('item_id') is None:
            print("没有消息id跳过")
            continue
        # 广告跳过
        elif item.get('label') == '广告':
            print("广告跳过")
            continue
        elif item.get('has_video') is True:
            print("视频跳过")
            continue
        else:
            id = item.get('item_id')
            title = item.get('title')
            source = item.get('source')
            abstract = item.get('abstract')
            publish_time = datetime.fromtimestamp(item.get('publish_time'))
            read_count = item.get('read_count', 0)
            share_count = item.get('share_count', 0)
            like_count = item.get('like_count', 0)
            comment_count = item.get('comment_count', 0)
            # print(item)

            comment = toutiao_comment(id)
            text, img_src= toutiao_detail(id)

            try:
                content = simple_chat_app(
                    prompt=title + text, comment=comment, model="ERNIE-Speed-128K", use_stream=False
                )
                # print(content)
                content = json.loads(content)

            except Exception as e:
                print(f"ai分析失败:{e} \n {title} \n {text} \n {comment}")
                continue

            message['唯一字段'] = tools.calculate_md5(title)
            message['新闻标题'] = title
            message['新闻来源'] = source
            message['新闻摘要'] = abstract
            message['新闻正文'] = text.replace('\n', '')
            message['新闻评论'] = comment

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
            message['评论分析'] = '' if comment_count == 0 else content.get('评论分析', '')

            message['发布时间'] = publish_time
            message['阅读数'] = read_count
            message['分享数'] = share_count
            message['点赞数'] = like_count
            message['评论数'] = comment_count
            message['图片列表'] = img_src


            print("*" * 100)
            print(message)
            print("*" * 100)


        # print(title)


        # print(item['content'])
        # print("\n\n\n\n\n\n\n\n\n\n\n")




if __name__ == '__main__':
    toutiao_list()
    # print(toutiao_comment("7410557522878186021"))

    # for i in range(1, 100):
    #     toutiao_list()

