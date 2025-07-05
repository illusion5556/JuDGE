# 创建多路检索方法的训练数据集
import json
from difflib import SequenceMatcher
from unittest import case

def are_strings_similar(str1, str2, threshold=0.85):
    """判断两个字符串是否相似度高于给定阈值"""
    similarity = SequenceMatcher(None, str1, str2).ratio()
    return similarity > threshold

# 读取 queries_train.json 文件，构建 text_id 到 text 的映射
def build_query_id_text_mapping(query_path):
    id_to_text = {}
    with open(query_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            text_id = item['text_id']
            text = item['text']
            id_to_text[text_id] = text
    return id_to_text

# 读取 queries_train.json 文件，构建 text_id 到 qw 的映射
def build_query_id_qw_mapping(query_path):
    id_to_qw = {}
    with open(query_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            text_id = item['text_id']
            qw = item['fd']
            id_to_qw[text_id] = qw
    return id_to_qw


# 读取 law-corpus.jsonl 文件，构建 CaseId 到 Fact 的映射
def build_law_id_text_mapping(law_corpus_path):
    id_to_text = {}
    with open(law_corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            CaseId = str(item['text_id'])
            name_n_text = f"{item['name']}：{item['text']}"
            id_to_text[CaseId] = name_n_text
    return id_to_text

# 读取 case_corpus.jsonl 文件，构建 CaseId 到 UUId 的映射
def build_case_id_uuid_mapping(case_corpus_path):
    id_to_uuid = {}
    with open(case_corpus_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for id, item in enumerate(data):
            id_to_uuid[str(id)] = item['CaseId']
    return id_to_uuid

# 读取 case_corpus.jsonl 文件，构建 CaseId 到 Fact 的映射
def build_case_id_text_mapping(case_corpus_path):
    id_to_text = {}
    with open(case_corpus_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            CaseId = item['CaseId']
            Fact = item['Fact']
            qw = item['Full Document']
            crime = item['Crime Type']
            prison = item['Sentence']
            laws = item['Law Articles']
            fine = item['Fine']
            id_to_text[CaseId] = (Fact, qw, crime, prison, laws, fine)

    return id_to_text

# 解析 runfile 并根据编号找到对应的 Fact 内容
def extract_law_texts(runfile_path, law_corpus_path):
    id_to_text = build_law_id_text_mapping(law_corpus_path)
    query_to_laws = {}
    
    with open(runfile_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            query_id = parts[0]
            law_id = parts[2]
            law_text = id_to_text.get(law_id, "")
            
            if query_id not in query_to_laws:
                query_to_laws[query_id] = []
            
            query_to_laws[query_id].append(law_text)
    
    return query_to_laws

# 解析 runfile 并根据编号找到对应的 Fact 内容
def extract_case_texts(runfile_path, case_corpus_path, law_corpus_path, queryID_to_text):
    id_to_text = build_case_id_text_mapping(case_corpus_path)
    # id_to_lawtext = build_law_id_text_mapping(law_corpus_path)
    id_to_uuid = build_case_id_uuid_mapping(case_corpus_path)
    query_to_ljp = {}
    query_to_qw={}
    with open(runfile_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            query_id = parts[0]
            case_id = parts[2]
            case_text, qw, crime, prison, law, fine = id_to_text[id_to_uuid[case_id]]
            
            law_text = []
            for law_id in law:
                law_text.append(id_to_lawtext.get(str(law_id), ""))

            query = queryID_to_text[query_id]
            if are_strings_similar(query, case_text):
                continue

            if query_id not in query_to_ljp:
                query_to_ljp[query_id] = []
            
            query_to_ljp[query_id].append({"fact":case_text, "crime":crime, "prison":prison, "laws":law_text, "fine":fine})
            if query_id not in query_to_qw:
                query_to_qw[query_id] = []
            query_to_qw[query_id].append(qw)
    
    return query_to_ljp,query_to_qw

def case_text(case):
    fact = case["fact"]
    crime = case["crime"]
    prison = case["prison"]
    law_text = case["laws"]
    fine = case["fine"]

    # case1 = f"""认定事实:{fact},罪名:{crime},法律条款:{law_text},刑期:{prison},罚金:{fine}"""
    case1 = f"""罪名:{crime},法律条款:{law_text},刑期:{prison},罚金:{fine}"""
    return "{" + case1 + "}"

# 示例调用
query_path = '../data/test.json'
queryId_to_text = build_query_id_text_mapping(query_path)
queryId_to_qw = build_query_id_qw_mapping(query_path)

law_runfile_path = '../reranker/score/test/reranker_run_file_test'  # 替换为实际路径
law_corpus_path = '../data/law_corpus.jsonl'  # 替换为实际路径
id_to_lawtext = build_law_id_text_mapping(law_corpus_path)
case_runfile_path = '../retriever/encode/sailer/run_file_test'  # 替换为实际路径
case_corpus_path = '../data/all_amend.json'


law_result = extract_law_texts(law_runfile_path, law_corpus_path)
case_result,qw_result = extract_case_texts(case_runfile_path, case_corpus_path, law_corpus_path, queryId_to_text)

jsonl_file_path = '../train/test_doc_nojudge.json'
queryId_to_ljp = build_case_id_text_mapping(case_corpus_path)
with open(jsonl_file_path, 'w') as jsonl_file:
    for query_id, laws in law_result.items():
        query_text = queryId_to_text[query_id]
        cases = case_result[query_id]
        qws=qw_result[query_id]
        # print(cases[0])
        case1 = case_text(cases[0])
        # case2 = case_text(cases[1])
        relevant_qw = "无相关判决书"
        # 找出所有符合长度要求的 qw
        suitable_qw = [qw for qw in qws if len(qw) <= 1500]
        
        if suitable_qw:
            relevant_qw = f"相关案例判决书：{suitable_qw[0]}"
        else:
            # 如果没有符合长度要求的 qw，则找出最短的那个
            shortest_qw = min(qws, key=len)
            relevant_qw = f"相关案例判决书：{shortest_qw}"
         

        all_laws = laws[:10] # 只取top10
        relevant_laws = "\n".join([f"{i+1}. {law}" for i, law in enumerate(all_laws)])

        template ="""×××人民法院
刑事判决书
(××××)×刑初字第××号
机关×××人民检察院。
被告人……(写明姓名、性别、出生年月日、民族、出生地、文化程度、职业或者工作单位和职务、住址和因本案所受强制措施情况等，现羁押处所)。
辩护人……(写明姓名、工作单位和职务)。
×××人民检察院以×检×诉〔〕××号起诉书指控被告人×××犯××罪，于××××年××月××日向本院提起。本院依法组成合议庭，公开(或者不公开)开庭审理了本案。×××人民检察院指派检察员×××出庭支持，被害人×××及其法定代理人×××、诉讼代理人×××，被告人×××及其法定代理人×××、辩护人×××，×××，鉴定人×××，翻译人员×××等到庭参加诉讼。现已审理终结。
×××人民检察院指控……(概述人民检察院指控被告人犯罪的事实、证据和适用法律的意见)。
被告人×××辩称……(概述被告人对指控的犯罪事实予以供述、辩解、自行辩护的意见和有关证据)。辩护人×××提出的辩护意见是……(概述辩护人的辩护意见和有关证据)。
经审理查明，……(首先写明经庭审查明的事实；其次写明经举证、质证定案的证据及其来源；最后对控辩双方有异议的事实、证据进行分析、认证)。
本院认为，……(根据查证属实的事实、证据和有关法律规定，论证机关指控的犯罪是否成立，被告人的行为是否构成犯罪，犯的什么罪，应否从轻、减轻、免除处罚或者从重处罚。对于控辩双方关于适用法律方面的意见，应当有分析地表示是否予以采纳，并阐明理由)。依照……(写明判决的法律依据)的规定，判决如下：
……〔写明判决结果。分三种情况：
第一，定罪判刑的，表述为：
“一、被告人×××犯××罪，判处……(写明主刑、附加刑)。(刑期从判决执行之日起计算。判决执行以前先行羁押的，羁押一日折抵刑期一日，即自××××年××月××日起至××××年××月××日止)。
二、被告人×××……(写明决定追缴、退赔或者发还被害人、没收财物的名称、种类和数额)。”
第二，定罪免刑的，表述为：
“被告人×××犯××罪，免予刑事处罚(如有追缴、退赔或者没收财物的，续写第二项)。”
第三，宣告无罪的，无论是适用《中华人民共和国》第一百六十二条第(二)项还是第(三)项，均应表述为：
“被告人×××无罪”。〕
如不服本判决，可在接到判决书的第二日起十日内，通过本院或者直接向×××人民法院提出上诉。书面上诉的，应当提交上诉状正本一份，副本×份。
审判长 ×××
审判员 ×××
审判员 ×××
(院印)
××××年××月××日
本件与原本核对无异
书记员 ×××""".replace('\n',' ')

        judgment_content = f"""
任务背景: 根据以下提供的相关案例、法律条款和案件事实，生成一份完整的刑法判决书。判决书需包括案件事实、法律分析、裁判理由以及最终裁判结论。\n
判决书的格式方面，请参考判决书模板：
{template}\n
以下是与本案件类似案例的判决书，可参考其格式及判决过程：
{relevant_qw}\n
以下是与本案件类似案例的初步裁判结论，其作为最终裁判结论的主要参考：
{case1}\n
请根据以上内容和下面的案件事实描述，为这个案件生成一份刑事判决书，结构完整，参考提供给你的判决书模板的格式（需包含案件事实陈述、法律分析、裁判理由及裁判结论等部分。不超过两千字。
本案件事实：{query_text}
本案件的完整判决书为：
"""
        # print("输入：", judgment_content)
        # print('-'* 100)
        # 将判决书内容写入 JSONL 文件
        ljp_res_tuple = queryId_to_ljp[query_id]
        crime=ljp_res_tuple[2]
        prison=ljp_res_tuple[3]
        laws=ljp_res_tuple[4]
        fine=ljp_res_tuple[5]
        law_text = []
        # for law_id in laws:
        #     law_text.append(id_to_lawtext.get(str(law_id), ""))
        # result_text = "{"+f"""罪名:{crime},法律条款:{law_text},刑期:{prison},罚金:{fine}"""+"}"
        record = {"caseid":query_id,"input": judgment_content.strip(), "output": queryId_to_qw[query_id]}
        jsonl_file.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"Data written to {jsonl_file_path}")