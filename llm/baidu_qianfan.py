import os
import qianfan
import json
import os
from dotenv import load_dotenv

# config = json.load(open('../env.json'))

# 加载 .env 文件
load_dotenv()

# 获取环境变量
QIANFAN_ACCESS_KEY = os.getenv('QIANFAN_ACCESS_KEY')
QIANFAN_SECRET_KEY = os.getenv('QIANFAN_SECRET_KEY')


# 【推荐】使用安全认证AK/SK鉴权，通过环境变量初始化认证信息
# 替换下列示例中参数，安全认证Access Key替换your_iam_ak，Secret Key替换your_iam_sk
os.environ["QIANFAN_ACCESS_KEY"] = QIANFAN_ACCESS_KEY
os.environ["QIANFAN_SECRET_KEY"] = QIANFAN_SECRET_KEY

chat_comp = qianfan.ChatCompletion()


def simple_chat(prompt, model, use_stream=False):
    # 指定特定模型
    max_retries = 6
    def is_valid_json(text):
        try:
            json.loads(text)
            return True
        except json.JSONDecodeError:
            return False

    for attempt in range(max_retries):
        resp = chat_comp.do(model=model,
                        stream=use_stream,
                        messages=[{
                            "role": "user",
                            "content": f'''你是一位数据分析师，现在需要你帮助分析数据。我会给你一则新闻，请你根据新闻的内容进行分析
                                       要求：
                                       1.情感分析：情感分析结果包括积极、消极、中性
                                       2.新闻行业：这则新闻主要涉及哪个行业?例如金融、科技、医疗、教育、政治等。
                                       3.所属国家：如涉及多个国家,请列出如果没有请返回“无”。
                                       4.涉及机构：新闻中提到的主要机构、组织和公司有哪些，多个机构用/分开。
                                       5.涉及人物：新闻中提到的关键人物有哪些?请列出他们的名字和职务，多个人名用/分开。
                                       6.事件影响：这则新闻报道的事件可能会对相关行业、公司和个人产生怎样的影响?请简要分析，如果无法得知事件影响，请返回“无”。
                                       7.关键词：从新闻中提取3个最重要的关键词，多个关键字用/分开。
                                       8.事件原因：新闻中的事件为什么会发生?有什么背景或触发因素? 如果无事件原因，请返回“无”。
                                       9.未来预测：基于目前的信息,这则新闻涉及的事件未来可能会如何发展，如果无法预测，请返回“无”。
                                       10.新闻概要：提取新闻的概要
                                       11.消息来源：对新闻进行综合分析，分析该新闻是否为官方, 小道, 未知

                                       输出格式：
                                       返回一个能被josn.loads函数处理的json格式的字典，格式如下：
                                       键值：情感分析、新闻行业、所属国家、涉及机构、涉及人物、事件影响、关键字、事件原因、未来预测、新闻概要、消息来源
                                       请严格按照格式输出，不要输出其他内容。
                                    新闻的内容是：{prompt}'''
                        }])
        result = resp["body"]["result"].replace("```json", "").replace("```", "").strip()

        if is_valid_json(result):
            return result
        else:
            if attempt == max_retries - 1:
                print(f"Failed to get a valid JSON response after maximum retries. Last response:",result)
            else:
                print(f"Attempt {attempt + 1} failed: Response is not valid JSON. Retrying...")

    raise ValueError("Failed to get a valid JSON response after maximum retries")

def news_summary(prompt, model, use_stream=False):
    # 指定特定模型
    resp = chat_comp.do(model=model,
                        stream=use_stream,
                        temperature=0.3,
                        # messages=[{
                        #     "role": "user",
                        #     "content": f'''你是一位资深炒股人员，善于从新闻资讯中分析会对股市产生波动的因素。请你分析今天的新闻资讯
                        #                 要求：
                        #                 1、综合所有新闻，在宏观经济层面给出短期内对整个市场可能造成的具体影响
                        #                 2、短期内在细分市场可能造成的影响和波动，以及引起波动的原因
                        #                 3、不要用markdown格式输出
                        #              今天的新闻有：{prompt}'''
                        # }])

                        messages=[{
                            "role": "user",
                            "content": f'''
                            你是一位专业的经济分析AI助手。我们有一批已经过初步处理的新闻数据，包含了新闻类型、所属行业和情感分析结果。你的任务是对这些数据进行深入分析，提供有价值的洞察和预测。请按照以下步骤进行分析：                 
                            1.跨行业关联
                            识别不同行业间的新闻关联性。分析一个行业的新闻如何可能影响其他相关行业。                           
                            2.趋势识别
                            从新闻数据中识别新兴的经济或市场趋势。预测这些趋势在未来几周或几个月可能的发展方向。                            
                            3.关键事件分析                            
                            识别可能对整体经济或特定行业产生重大影响的关键新闻事件。评估这些事件的潜在影响范围和持续时间。                                                      
                            4.政策影响评估                            
                            识别与经济政策相关的新闻。分析这些政策新闻可能对不同行业和整体经济产生的影响。
                            5.风险识别
                            基于新闻数据，识别潜在的经济或市场风险。提出可能的风险缓解策略建议。
                            6.机会洞察
                            从新闻中识别潜在的投资或商业机会。解释为什么这些机会值得关注，以及如何可能从中获益。
                            7.预测性分析
                            基于当前的新闻趋势，对未来一周到一个月的经济和市场走向进行预测。说明这些预测的依据和可能影响预测准确性的因素。
                            8.行动建议
                            基于你的分析，为不同类型的经济参与者（如投资者、企业、政策制定者）提出具体的行动建议。
                            
                            请确保你的分析深入、客观，并提供具体的例子支持你的观点。如果某些领域的信息不足以得出结论，请指出这一点并建议可能需要的额外数据。
                            你的分析将用于辅助重要的决策制定，因此准确性和洞察力至关重要。
                        今天的新闻有：{prompt}'''
                        }])
    # print(resp["body"])
    return resp["body"]["result"]


def simple_chat_app(prompt, comment, model, use_stream=False):
    max_retries = 6
    # 指定特定模型
    def is_valid_json(text):
        try:
            json.loads(text)
            return True
        except json.JSONDecodeError:
            return False

    for attempt in range(max_retries):
        resp = chat_comp.do(model=model,
                            stream=use_stream,
                            messages=[{
                                "role": "user",
                                "content": f'''你是一位数据分析师，现在需要你帮助分析数据。我会给你一则新闻和若干新闻评论，请你根据新闻的内容和新闻的评论进行分析
                                           要求：
                                           1.情感分析：情感分析结果包括积极、消极、中性
                                           2.新闻行业：这则新闻主要涉及哪个行业?例如金融、科技、医疗、教育、政治等。
                                           3.所属国家：如涉及多个国家,请列出如果没有请返回"无"。
                                           4.涉及机构：新闻中提到的主要机构、组织和公司有哪些，多个机构用/分开。
                                           5.涉及人物：新闻中提到的关键人物有哪些?请列出他们的名字和职务，多个人名用/分开。
                                           6.事件影响：这则新闻报道的事件可能会对相关行业、公司和个人产生怎样的影响?请简要分析，如果无法得知事件影响，请返回"无"。
                                           7.关键词：从新闻中提取3个最重要的关键词，多个关键字用/分开。
                                           8.事件原因：新闻中的事件为什么会发生?有什么背景或触发因素? 如果无事件原因，请返回"无"。
                                           9.未来预测：基于目前的信息,这则新闻涉及的事件未来可能会如何发展，如果无法预测，请返回"无"。
                                           10.新闻概要：提取新闻的概要
                                           11.消息来源：对新闻进行综合分析，分析该新闻是否为官方, 小道, 未知
                                           12.评论分析：对评论进行分析，概括评论在说什么，给出一个情感分析结果，包括积极、消极、中性，并给出一个理由。

                                           输出格式：
                                           返回一个能被josn.loads函数处理的json格式的字典，格式如下：
                                           键值：情感分析、新闻行业、所属国家、涉及机构、涉及人物、事件影响、关键词、事件原因、未来预测、新闻概要、消息来源、评论分析
                                           请严格按照格式输出，不要输出其他内容。
                                        新闻的内容是：{prompt}
                                        新闻的评论是：{comment}
                                        '''
                            }])

        result = resp["body"]["result"].replace("```json", "").replace("```", "").strip()

        if is_valid_json(result):
            return result
        else:
            if attempt == max_retries - 1:
                print(f"Failed to get a valid JSON response after maximum retries. Last response:",result)
            else:
                print(f"Attempt {attempt + 1} failed: Response is not valid JSON. Retrying...")

    raise ValueError("Failed to get a valid JSON response after maximum retries")


def simple_chat_app_self(prompt, comment, model, use_stream=False):
    max_retries = 6
    # 指定特定模型
    def is_valid_json(text):
        try:
            json.loads(text)
            return True
        except json.JSONDecodeError:
            return False

    for attempt in range(max_retries):
        resp = chat_comp.do(model=model,
                            stream=use_stream,
                            messages=[{
                                "role": "user",
                                "content": f'''你是一位数据分析师，现在需要你帮助分析数据。我会给你一篇消息和针对该消息的若干评论，请你根据消息和评论进行分析
                                           要求：
                                           1.情感分析：消息的情感分析，结果包括积极、消极、中性
                                           2.新闻行业：消息所涉及哪个行业?例如金融、科技、医疗、教育、政治等。
                                           3.所属国家：如涉及多个国家,请列出，如果没有请返回"无"。
                                           4.涉及机构：消息中提到的主要机构、组织和公司有哪些，多个机构用/分开，如果没有请返回"无"。
                                           5.涉及人物：消息提到的关键人物有哪些?请列出他们的名字和职务，多个人名用/分开，如果没有请返回"无"。
                                           6.事件影响：消息说提到的事件可能会对相关行业、公司和个人产生怎样的影响?请简要分析，如果无法得知事件影响，请返回"无"。
                                           7.关键词：从消息中提取3个最重要的关键词，多个关键字用/分开。
                                           8.事件原因：消息中的事件为什么会发生?有什么背景或触发因素? 如果无事件原因，请返回"无"。
                                           9.未来预测：基于目前的信息，这则消息涉及的事件未来可能会如何发展，如果无法预测，请返回"无"。
                                           10.新闻概要：提取消息的概要
                                           11.消息来源：对消息的发布来源进行综合分析，分析该消息是官方, 小道, 未知
                                           12.评论分析：对评论进行分析，概括评论在说什么，给出一个情感分析结果，包括积极、消极、中性，并给出一个理由。

                                           输出格式：
                                           返回一个能被josn.loads函数处理的json格式的字典，格式如下：
                                           键值：情感分析、新闻行业、所属国家、涉及机构、涉及人物、事件影响、关键词、事件原因、未来预测、新闻概要、消息来源、评论分析
                                           请严格按照格式输出，不要输出其他内容。
                                        消息的内容是：{prompt}
                                        消息的评论是：{comment}
                                        '''
                            }])

        result = resp["body"]["result"].replace("```json", "").replace("```", "").strip()

        if is_valid_json(result):
            return result
        else:
            if attempt == max_retries - 1:
                print(f"Failed to get a valid JSON response after maximum retries. Last response:",result)
            else:
                print(f"Attempt {attempt + 1} failed: Response is not valid JSON. Retrying...")

    raise ValueError("Failed to get a valid JSON response after maximum retries")


if __name__ == "__main__":
    prompts = [
        "【招银国际：维持快手“买入”评级 目标价为97港元 对盈利增长空间有信心】招银国际发表报告指出，在618促销活动中，快手强调低价好货的产品、更简单的方式和更长的周期。该行认为，快手电商泛货架业务表现良好，订单及付费用户分别按年增长65%及57%。该行预期，快手电商泛货架业务的商品交易总额(GMV)占比将超过25%，今年次季的电商业务增长将保持不变，预期GMV与其他服务收入按年增长25%及24 %。尽管第三方行业数据显示喜坏参半，但该行看好快手618的份额增长，并预期随着毛利率持续改善，对快手的盈利增长空间充满信心。该行维持对快手“买入”评级，目标价为97港元。",
        "【字节跳动回应与博通合作开发AI芯片：该消息不实】 6月24日，有市场消息称，字节跳动将与美国芯片设计公司博通合作开发AI芯片，对此，字节跳动表示，该消息不实。",
        "【卫星化学α-烯烃综合利用高端新材料产业园启动建设】6月24日上午，卫星化学在江苏连云港徐圩新区投资建设的国内首个α-烯烃综合利用高端新材料产业园项目正式启动建设。该项目总投资266亿元，项目采用自主研发的高碳α-烯烃技术，向下游延伸高端聚烯烃、聚烯烃弹性体、润滑油基础油、超高分子量聚乙烯等高端新材料。",
        "【长城汽车与华为签署《HUAWEI HiCar 集成开发合作协议》】 据长城汽车消息，近日，在2024年华为开发者大会上，长城汽车与华为签署《HUAWEI HiCar 集成开发合作协议》。根据《协议》，长城汽车将成为首批获得HUAWEI HiCar产品源代码、开发工具等深度开发资源的汽车公司。在此基础上，双方团队将进一步打造共创共赢的开发生态。一方面，通过共享资源与技术专长，HUAWEI HiCar相关产品在长城汽车多款产品上的适配将显著加速，实现从单一车型到全系车型无缝对接，提升适配的广度与深度，不断提升用户的车载智能体验。另一方面，双方团队将共探产品升级，研发更多前沿能力，不断丰富用户行车体验，使手车互联不再是简单连接，而成为真正意义上的智能协同。",
        "【金岭矿业：子公司金钢矿业采矿权延续完成】 金岭矿业(000655)6月24日晚间公告，公司收到子公司塔什库尔干县金钢矿业有限责任公司（简称“金钢矿业”）的通知，金钢矿业已完成采矿权延续相关材料的补充工作，并取得了金钢矿业采矿许可证，有效期限5年（自2024年2月29日至2029年2月28日）。",
        "【突破200亿元 多只头部宽基ETF成交额持续放量】A股指数今日全天调整，三大股指均跌超1%。值得注意的是，多只头部宽基ETF成交额持续放量。其中，华泰柏瑞沪深300ETF单日成交额突破70亿元，以73.15亿元领跑市场。南方中证500ETF、华夏上证50ETF紧随其后，单日成交额达到42.19亿元、31.23亿元。此外，华夏上证科创板50成份ETF、嘉实沪深300ETF等单日成交额也都超过20亿元。整体来看，成交额前五的宽基ETF单日成交累计突破200亿元。（中证金牛座）",
        "新加坡海峡时报指数涨0.2%至3,314.14点。",
        "马来西亚富时隆综指基本持平于1,589.66点。",
        "青海公布2024年高考分数线。",
        "【长沙地铁2、3号线恢复运营】@长沙地铁 发布运营公告：尊敬的乘客朋友，伴随雨势减弱，并经工作人员全力抢修，自6月24日17:30起，长沙地铁2、3号线除长沙火车站、橘子洲站仍实施跳站（列车不停站通过）外，其余站点（含西环线站点）均恢复正常运营。如遇个别垂梯、扶梯等设备不能正常使用情况，敬请谅解。",
        "【海南儋州：在海南省实际居住满183天，购房享本地居民同等待遇】 6月24日，海南省儋州市住房和城乡建设局发布《关于进一步调整房地产政策措施的通知》。文件提出，支持常住人口购房需求。落户海南省户籍的，自落户之日起，在儋州市购房享本地居民同等待遇；非本省户籍人员，但在海南省实际居住满183天的常住人口，在儋州市购房享本地居民同等待遇。同时，支持企事业单位员工及人才购房需求。对符合儋州市重点企事业单位条件的企业，根据企业投资、纳税贡献、实际住房需求等情况，梯次匹配一定比例的非本省户籍居民家庭购房指标。",
        "【广东佛山：进一步减轻购房压力，公积金缴存余额倍数提至16倍】 近日，广东省佛山市住房公积金管理中心发布《关于调整个人住房公积金贷款有关事项的通知》，将缴存余额倍数由原来的12倍调整为16倍。该新政从2024年7月1日起施行，自施行日起受委托银行受理的贷款申请按新标准执行，有效期为5年。通知显示，佛山市公积金贷款首付款比例应当不低于20%。同时，遵循“先存后贷、存贷挂钩”的原则，佛山市公积金贷款实行差别化贷款，即不同缴存时间对应不同的最高贷款额度。夫妻共同申请公积金贷款且符合公积金贷款条件的，缴存时间的认定以主借款申请人为准。在佛山市缴存住房公积金的高层次人才申请公积金贷款时，缴存时间按≥36个月认定。",
        "【广东：1—5月，全省商品房销售面积同比下降34%】 据广东统计局，1—5月，全省房地产开发投资0.46万亿元，同比下降16.7%，降幅比1—4月扩大2.5个百分点。其中，商品住宅投资下降19.5%，办公楼投资增长2.2%，商业营业用房投资下降8.8%。分区域看，珠三角地区房地产投资下降15.1%；粤东粤西粤北地区房地产投资合计下降25.9%。1—5月，全省商品房销售面积同比下降34.0%。",
        "【生意社：宏观利空情绪消退 铜价止跌回暖】上周铜价先跌后涨，截止周末现货铜报价79428.33元/吨，较周初的78791.67元/吨上涨0.81%，同比上涨14.1%。宏观利空情绪逐渐消退，市场情绪有所转暖。前期铜价回落提振下游消费，铜矿短缺恶化程度或超预期，市场对原料短缺的担忧持续存在，国内炼厂或在三季度末开启减产。在新能源领域高增长的带动下，铜消费整体韧性较强，但传统下游仍然低迷。预计短期内铜市场震荡为主。",
        "A股科创次新股震荡走低，锴威特跌超14%，逸飞激光、泰凌微、安凯微、信宇人、盛邦安全、艾罗能源等跟跌。",
        "【收评：指数调整三大股指均跌超1% 两市近5000只个股下跌】指数全天调整，三大股指均跌超1%，北证50指数跌超3%。板块方面，电力板块局部走强，西昌电力封涨停，乐山电力、明星电力涨幅居前；证金持股概念部分活跃，濮耐股份、海天味业等领涨；科创次新股全天走低，锴威特跌超10%；混合现实板块走弱，岭南股份跌停封板；脑机接口板块集体调整，力合科创跌停。总体来看，个股呈普跌态势，近5000只个股下跌。 盘面上，两市板块普跌，科创次新股、混合现实、脑机接口板块跌幅居前。",
        "【多路资金借道入场 370多亿元涌入股票型ETF】ETF在持续壮大中。近日，首批中证国新港股通央企红利ETF、首批科创100增强策略ETF均启动发行，首批投资沙特市场的ETF也火速敲定发行档期。从ETF持有人来看，国新投资认购了首批中证国新港股通央企红利ETF首发份额。此外，存量ETF也强势吸金。5月23日以来，已有370多亿元借助股票型ETF入市。",
        "摩根士丹利债券多头加码印度押注，截至5月底3.6%的摩根大通指数资产已配置在印度债券。",
        "JEFFERIES：将马拉松石油目标价从217美元上调至222美元。",
        "【报道：欧盟设计法律应变方案 绕过匈牙利在援乌问题上的否决权】英国金融时报援引欧盟首席外交官Josep Borrell的话报道称，对于动用俄罗斯冻结资产今年所产生利润来为乌克兰购买武器这个问题，欧盟设计了一个法律变通方案，以绕开匈牙利在此事上的否决权。报道援引Borrell的话说，匈牙利“不应该参与对这笔资金使用问题的决定”，因为该国在先前将俄罗斯冻结资产的收益留置的协议中弃权。匈牙利发言人不予置评。",
        "【云南德宏州：拟对参与住房“以旧换新”的业主补贴50%契税，支持地方国企收购已建成未出售商品住房】据德宏州政府官网，德宏州政府发布关于公开征求《关于优化调整房地产市场调控措施的通知（征求意见稿）》。其中指出，推行商品住房以旧换新支持房地产开发企业与房地产经纪机构合作实施“以旧换新”，更好满足人民群众高品质住房消费需要。实施“以旧换新”期间，在享受财政部、税务总局、住房城乡建设部支持居民换购住房有关个人所得税优惠政策和《德宏州促进房地产市场健康平稳发展工作措施》所提出的相关购房补贴等措施的同时，将购房补贴政策延伸至存量房交易市场，购买存量商品住房的业主可享受缴纳契税额50%的购房补贴，单套住宅补贴限额不超过2万元。同时，鼓励房地产企业对“以旧换新”的消费者给予相应的购房优惠和佣金抵扣房款；鼓励房地产企业回收居民旧房，并将旧房价款抵扣购买新房的购房款等政策。",
        "【广东：统筹构建规范高效的数据交易场所】近日，中共广东省委办公厅、广东省人民政府办公厅印发《关于构建数据基础制度推进数据要素市场高质量发展的实施意见》。其中提出，统筹构建规范高效的数据交易场所。构建多层次数据要素市场交易体系，推动区域性、行业性数据流通使用。推动广州、深圳数据交易所完善体系架构。强化公共属性和公益定位，推进数据交易场所与数据商功能分离。建立健全数据交易配套服务机构，建设行业性数据交易配套服务平台。鼓励在依法设立的数据交易机构开展数据流通、交易。推动政府通过数据交易场所开展数据采购活动。积极融入全国数据要素统一大市场，加强与省外数据交易场所、平台合作，实现数据产品“一所挂牌，多地同步发布、同步展示、同步交易”。",
        "【李德仁、薛其坤获2023年度国家最高科学技术奖】2023年度国家最高科学技术奖6月24日在京揭晓，李德仁院士、薛其坤院士获得中国科技界崇高荣誉。李德仁是著名的摄影测量与遥感学家，一直致力于提升我国测绘遥感对地观测水平。他攻克卫星遥感全球高精度定位及测图核心技术，解决了遥感卫星影像高精度处理的系列难题，带领团队研发全自动高精度航空与地面测量系统，为我国高精度高分辨率对地观测体系建设作出了杰出贡献。薛其坤是凝聚态物理领域著名科学家，取得多项引领性的重要科学突破。他率领团队首次实验观测到量子反常霍尔效应，在国际上产生重大学术影响；在异质结体系中发现界面增强的高温超导电性，开启了国际高温超导领域的全新研究方向。",
    ]
    for prompt in prompts:
        pass
    #     # Yi-34B-Chat
    #     # ERNIE-Speed-128K
    #     # ERNIE Speed-AppBuilder
    #     # ERNIE-Lite-8K-0922
    #     content = simple_chat(prompt=prompt, model="ERNIE-Speed-128K", use_stream=False)
    #     print(content)

    prompt = """
欧盟将从其“团结基金”中拨款4.3亿欧元，帮助斯洛文尼亚从一年前的洪水灾害中恢复重建。
刚刚过去的8月，上海一、二手住房成交量呈现持续增长态势，同比增长14%。数据显示居民购房贷款比例也有所提高。未来，上海楼市有望继续保持回升态势。
中央气象台发布了高温黄色预警，预计多个地区将出现高温天气，包括安徽南部、江苏南部等地区，最高气温可能达到40度以上。
法国轨道交通设备制造商阿尔斯通已完成将其北美传统信号业务出售给克诺尔集团的交易。此次交易对阿尔斯通的财务状况和克诺尔集团的业务领域将产生影响。
印度股市表现强劲，NIFTY指数收盘涨0.15%，报25,273.30点。同时，SENSEX指数也上涨0.24%，报82,559.84点，并创下历史新高。这可能对印度股市和全球股市产生积极影响。
深交所终止了宝通科技的特定对象发行股票审核，原因是公司和保荐人中信建投主动撤回了申请文件。此事件可能会对公司的融资计划和未来发展产生影响。
中国证券业协会发布了新的《证券从业人员职业道德准则》，包括诚实守信、专业尽职、以义取利、珍惜声誉、稳健审慎、致力长远、守正创新、益国利民、依法合规、廉洁自律、尊重包容等六项从业人员应遵守的行业道德准则。该准则已经理事会审议通过并报中国证监会备案，自发布之日起实施。
爱司凯公司在公告中披露，其涉及的3D打印技术目前尚处于小试阶段，市场拓展存在不确定性。该新闻涉及科技行业，可能会对公司的业务拓展和投资者对公司的估值产生影响。
华铁应急公告，公司骨干团队计划增持公司股份，增持金额不低于1亿元，不超过2亿元，实施期限为自公告披露日起6个月内。
健康元公司拟回购股份，回购金额预计为人民币3亿元至5亿元，旨在减少注册资本。预计回购期限为自股东大会审议通过后的一年。公司打算使用自有资金或自筹资金进行回购。
天成自控发布公告称，公司正在开发垂直起降飞行器的座椅业务，但尚处于开发阶段，短期内不会产生收入。公司现有主营业务以工程商用车座椅、乘用车座椅、飞机座椅为主，未来项目开发进度和取证时间存在不确定性。
建设银行副行长表示该行总体资产质量稳定，在房地产领域实现不良贷款额和不良率双降。他指出房地产供需两端的政策效应逐渐释放，市场出现积极变化。同时，该行也稳妥有序地做好地方债务风险的防范化解。新闻对房地产市场未来发展持乐观态度。
中国光伏行业协会组织召开“光伏电站建设招投标价格机制座谈会”，讨论光伏电站建设招投标过程中存在的价格问题，提出优化建议，以推动光伏行业的持续健康发展。
联合国近东巴勒斯坦难民救济和工程处表示，其在加沙地带的70%以上学校已被摧毁或损坏，导致数十万流离失所的家庭失去教育和避难场所。该事件反映出加沙地带的人道主义危机需要更多的国际支持来重建学校和社区。
韩国今年前七个月泡菜进口额创下新高，打破历史纪录。数据显示泡菜进口额和进口量均有所增加，表明韩国泡菜在全球市场上受欢迎。预计未来韩国泡菜出口将继续增长。
央行数据显示，国家开发银行、中国进出口银行、中国农业发展银行在2024年8月净归还抵押补充贷款778亿元，期末抵押补充贷款余额为26541亿元。这一数据可能反映出现阶段金融机构对抵押补充贷款的需求变化，对未来货币政策走向产生影响。
中国人民银行宣布对金融机构开展规模为3000亿元的中期借贷便利操作，期限一年，利率为2.30%，旨在维护银行体系流动性合理充裕。此次操作有助于稳定市场预期和促进货币市场的平稳运行。
商务部声明，未发布关于以旧换新惠民款补贴发放的公证通知，未组织相关直播宣讲活动，提醒消费者避免上当受骗。商务部已向公安机关报案。
人民银行在2024年8月对金融机构进行了常备借贷便利操作，旨在满足其临时流动性需求。期末常备借贷便利余额为0，利率发挥了利率走廊上限的作用，有助于维护货币市场利率平稳运行。
据上交所企业上市服务微信公众号消息，上周（8月26日—9月1日）无新增IPO申报企业。今年截至9月1日，新增申报企业共计32家。
上海金融法院公开开庭审理一起涉及非公开定向债务融资工具（PPN）的证券虚假陈述责任纠纷案件。该案是全国首例涉PPN证券虚假陈述纠纷案件，涉及多个金融机构和律师事务所等机构的责任问题。
*ST汉马公司公布2024年8月中重卡销量，同比增长4.56%。产量为704辆，同比增长7.15%。这表明市场对该公司产品的需求正在增长，对公司未来的业务发展有积极影响。
工信部发布轻工业数字化转型实施方案征求意见稿，提出编制轻工行业设备更新指南，推动关键设备和工艺数字化改造升级，加快网络通信技术应用，并建立健全网络安全和数据安全防护机制。
工信部发布《轻工业数字化转型实施方案（征求意见稿）》，提出到2027年轻工骨干企业基本实现数字化改造全覆盖的目标。该实施方案将推动轻工业数字化转型，提高生产效率和企业竞争力。
南向资金今日净买入超119亿港元，其中盈富基金等获得大量净买入，而腾讯控股和工商银行等则遭净卖出。这反映了市场对香港股票的投资动向。
交易商表示，与8月份计划的105万吨相比，俄罗斯从黑海港口图阿普谢出口的石油产品在9月计划达到97.8万吨。这一数据的变化可能受到多种因素的影响，并可能对全球石油市场产生影响。
腾讯控股在2日耗资约10.03亿港元回购了约265万股股份，回购价格为每股376.6港元至383.2港元之间。该行为可能旨在提振市场信心和提升公司股价。
九典制药近日收到国家药品监督管理局下发的吲哚布芬片药品注册证书，这将有利于公司市场拓展和产品销售，体现其在研发和创新方面的实力。
中荣股份计划使用不低于2500万元，不超过5000万元的自有资金回购股份，回购的股份将用于股权激励计划或员工持股计划。预计回购股份约占公司总股本的0.59%至1.17%。
贵州省黔西南州人大常委会原党组副书记、副主任张谦因受贿罪被判处有期徒刑十一年，并处罚金一百万元，其所得及其孳息将被追缴上缴国库。
科林电气公告，公司选举陈维强为董事长，史文伯为副董事长，并聘任王永为公司总经理。这是公司正常的管理层换届，旨在确保公司运营的连续性和稳定性。
国务院办公厅印发《关于以高水平开放推动服务贸易高质量发展的意见》，提出5方面20项重点任务，包括推动服务贸易制度型开放、促进资源要素跨境流动、推进重点领域创新发展等。
邮储银行副行长徐学明表示，商业银行面临息差压力，但下行趋势可能放缓。他认为商业银行需要一个相对合理的息差空间以保持利润增长，实现资本补充和风险覆盖，并服务于实体经济和长期可持续发展。
杭州银行宣布，国家金融监督管理总局浙江监管局已正式核准章建夫担任公司副行长的任职资格。未来，章建夫可能会为杭州银行的业务发展和管理改革做出重要贡献。
中国机电商会回应加拿大拟对中国电动汽车征收100%附加税，表示此举严重违反WTO规则，干扰全球绿色转型发展进程，将对中国出口企业造成重大损失。中国机电商会对此感到震惊和不解。
南非政府宣布将于9月4日下调汽油价格，每升下调0.92兰特，此举旨在减轻消费者负担，对能源行业和汽车行业可能产生一定影响。
美思德股东金致成计划减持不超过180万股，即不超过公司总股本的0.9828%，可能对公司股价产生影响。
浙商银行表示，上半年公司贷款资产质量稳定，零售贷款质量改善。展望2024年，房地产业仍是主要风险压力来源之一，受经济环境和房价下跌影响，小微企业和零售客户的信用风险持续上升。该行将加强风险管理并关注行业动态。
维尔利公司成功中标包头永和新材料公司的水处理系统项目，中标金额为1.48亿元。这次中标将对公司收入、业绩和行业声誉产生积极影响。
真兰仪表公告，公司与特瑞斯能源装备股份有限公司签署了《战略合作框架协议》，双方将结合自身需求和优势进行战略合作，共同推动相关领域的发展。
高德重启顺风车业务，目前已开通65个城市。未来可能会继续扩大业务范围和优化服务质量，满足用户多样化的出行需求。
梦百合公司西班牙生产基地从西班牙向美国出口的床垫产品被征收4.61%的反倾销税。但公司已在美国本土布局产能，且泰国生产基地未受影响。公司对未来的生产、经营保持乐观态度。
王府井集团与北京首都机场商贸有限公司哈尔滨分公司签署了两个机场的免税店项目合同，经营期限为10年。合同规定了保底经营费和商品销售额提取比例。
保隆科技获得欧洲某知名主机厂空气悬架系统产品项目定点通知书，成为其零部件供应商，预计生命周期总金额超过人民币2.4亿元，实现中国本土乘用车空气弹簧供应商在欧洲项目的首次突破。
宁德时代发生大宗交易，成交折价率达18.61%，买方和卖方营业部分别为华林证券股份有限公司和方正证券股份有限公司的某些营业部。
国缆检测总经理黄国飞因工作安排原因辞职，离任后将继续担任公司董事职务。
贵州茅台公告，将于2024年9月9日召开半年度业绩说明会。
惠誉确认华润置地的评级为'BBB+'，展望稳定。这一评级将增强华润置地在资本市场的竞争力，为其未来的融资和业务发展提供支持。
日本政府计划对未能达到温室气体减排目标的企业进行罚款，旨在促进企业减少排放并推动环保行动。
据俄罗斯国防部报告，俄罗斯军队已控制乌克兰东部的斯库奇涅。
安徽省人民政府国有资产监督管理委员会原副主任杨东坡涉嫌严重违纪违法，目前正在接受安徽省纪委监委纪律审查和监察调查。
    """

    # content = news_summary(prompt=prompt, model="ERNIE-Speed-128K", use_stream=False)
    # print(content)


    prompt = """
华为门店销售劝退：没必要加价10万买一台 等着就行了 
 据媒体报道，9月10日，华为Mate XT 非凡大师在华为商城预售已超400万人预约。对此，华为手机授权门店客服人员表示：“即便现在10万一台，咱不需要，咱就不买，等什么时候官网下单直接买到。就像现在华为MateX5，不仅能买到，还有更多的优惠，不也挺好的吗？提前两三个月购买没那必要。等着就行了。”至于华为Mate XT非凡大师何时能进行大批量线下售卖，该位人员指出，目前还没有接到通知。“我要是知道什么时候大批量出售，什么时候小批量出售，什么时候会便宜出售，那就和预测股票一样了。”（东方网·纵相视频 巢思远）延伸阅读相比万年不变的苹果手机，华为的三折叠手机Mate XT成为了最近两场手机巨头发布会中的最大亮点。Mate XT非凡大师被定位为“超高端手机”，起售价高达19999元。这款手机搭载一块10.2英寸屏幕，展开厚度为3.6毫米，是目前行业内最薄的折叠屏手机。Mate XT非凡大师出生自带噱头，作为全球首款量产的三折叠手机，从9月7日开启预定后，就在市场中掀起了一阵狂热追捧。根据华为线上商城显示，在不到24小时的时间内，Mate XT非凡大师的预约数量逼近200万。截止9月10日10:00时，其预约人数已经超过480万，并还在快速增长。而在京东、天猫的华为自营旗舰店开放的预约渠道中，页面显示的加购人数也超过了百万。9月7日下午2点半，记者在深圳坂田华为全球旗舰店实探发现，前来预约的消费者排起长队（图/海报新闻）一位华为门店销售向Tech星球表示，从开启预约至今，门店每天都在排队登记预约意向，并且在发布会之后，样机到店展示时，因为客流过爆，目前上手体验也需要提前预约。不过该门店销售人员表示，现在还没有开放购买，第一批货要在20日开售。去年华为Mate 60系列曾掀起一阵抢购热潮，延续至Mate XT非凡大师热度则更甚。于是，在用户狂热期待中，“黄牛”们看到了巨大的商机，连同代理商、经销商们，一同盯上了Mate XT非凡大师的溢价空间。2万起售价，7万的溢价“大多数人拿不到首轮新机”，一位华为经销商称，无论是线上商城、线下还是电商渠道，所开放的预定只是意向统计，而非排序购买的资格。一位门店工作人员也告诉Tech星球，现阶段预订的确是登记意向，后续到货后要进行抽签决定。另一个门店的销售则表示，从发布当天至今，因为过于火爆，门店已经停止了预约登记。在二手交易平台闲鱼、得物，以及抖音上，华为三折叠的大量预订订单出现转
    
    """

    comment = """
  销售心想：明年过时降价了都没人买
还好我买不起
华为人人善良！👍
哈哈哈哈，中国真好玩[斜眼笑][大笑]
你有购买华为手机的打算吗
你觉得华为三折是不是太贵了
华为Mate XT三折叠手机你喜欢吗？
华为手机和苹果手机，你喜欢哪一个
高价手机是否真的值得购买？
那怎么办，CPU芯片都是保密的，哈哈哈[大笑]
脑子得进多少水，花十万买这个
奈何喜欢装逼的都是“低层”，嘿嘿！
有傻逼加价，为啥不敢卖？真是的
这是正解，冲动消费要不得，买东西，跟自己的需求和喜爱，更主要还是自己的经济能力来！
有必要加价买华为折叠手机吗
喜欢5G的
日你M的软文，骗傻子呢，还十万？你想呢！
何时这样的新闻没有了、那时候才是华为手机真正最强大的时代！
就跟当初外折还是内折屏幕一样[狗]为为用啥啥就是最好的
继续炒作
为什么不给加价？
    
    """
    # content = simple_chat_app(prompt=prompt, comment=comment, model="ERNIE-Speed-128K", use_stream=False)
    # print(content)

    prompt = """
title:有人说天津机场上空出现的就是这个东西？TR3B反重力武器？
看到有人猜测天津机场并不是无人机作怪，而是有这种说法。好像美国这个武器真的存在，能够悬停那么久就不一般。据说又造成天津机场短暂停飞？text:有人说天津机场上空出现的就是这个东西？TR3B反重力武器？
看到有人猜测天津机场并不是无人机作怪，而是有这种说法。好像美国这个武器真的存在，能够悬停那么久就不一般。据说又造成天津机场短暂停飞？
    """

    comment = """
如果真的能逼着美国拿出新玩意出来，说明目前美国拿我们没办法了。 | 7
如果是国外的飞行器，或是国外的高精尖飞行器，我们早就打下来，然后拿走研究了。所以别说是国外的东西。 | 2
天津防空 军方一句话也没有吗？ | 1
就是出来炫肌肉，如果你敢升空，它说不定真敢搞事情，所以避免直接冲突，先只能在下面观察情况 | 1
天津好像还有个别名叫“天津卫”吧…… | 1
这么牛逼的东西出来就为了吓唬？不藏起来打仗杀个措手不及？ | 1
大家过来看，这是什么类型铅笔 | 0
我们的高空气球也具备这实力 | 0
不可能进入我国领空 | 0
得了吧，要是美国有这东西绝对不会藏着掖着，哪怕只有个PPT都要拿出来秀的，要真有这玩意儿，在它被造出来的那一刻就得喊上各种BC现场直播了 | 0
不说是风筝吗 | 0
据说上个世纪九十年代美国就已经掌握了反重力飞行技术，但作为技术储备一直没有正事运行 | 0
那干嘛不找个没人的地儿做实验？还是说就拿民航客机做实验，要不就是怕美国人不知道我们有这个技术→_→ | 0
美国在秀肌肉 | 0
转发了 | 0
转发了 | 0
转发了 | 0
如果是反重力武器，已经入侵中国领空，直接打下来。 | 0
为什么不来广州白云机场，全世界最大的机场，是因为广州有大量的摄影发烧友，长距大炮人手一个，可以拍得一清二楚？不像某地只有手机拍照。 | 0
笑死了 | 0
"""

    content = simple_chat_app_self(prompt=prompt, comment=comment, model="ERNIE-Speed-128K", use_stream=False)
    print(content)
