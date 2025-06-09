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
    
    return query_to_ljp

def case_text(case):
    fact = case["fact"]
    crime = case["crime"]
    prison = case["prison"]
    law_text = case["laws"]
    fine = case["fine"]

    case1 = f"""认定事实:{fact},罪名:{crime},法律条款:{law_text},刑期:{prison},罚金:{fine}"""
    return "{" + case1 + "}"

suffix = "train"
# 示例调用
query_path = f'../data/{suffix}.json'
queryId_to_text = build_query_id_text_mapping(query_path)
# queryId_to_qw = build_query_id_qw_mapping(query_path)

law_runfile_path = f'../reranker/score/{suffix}/reranker_run_file_{suffix}'  # 替换为实际路径
law_corpus_path = '../data/law_corpus.jsonl'  # 替换为实际路径
id_to_lawtext = build_law_id_text_mapping(law_corpus_path)
case_runfile_path = f'../retriever/encode/sailer/run_file_{suffix}'  # 替换为实际路径
case_corpus_path = '../data/all_amend.json'


law_result = extract_law_texts(law_runfile_path, law_corpus_path)
case_result = extract_case_texts(case_runfile_path, case_corpus_path, law_corpus_path, queryId_to_text)

jsonl_file_path = f'../train/{suffix}_ljp.json'
queryId_to_ljp = build_case_id_text_mapping(case_corpus_path)
with open(jsonl_file_path, 'w') as jsonl_file:
    for query_id, laws in law_result.items():
        query_text = queryId_to_text[query_id]
        cases = case_result[query_id]
        # print(cases[0])
        case1 = case_text(cases[0])
        # case2 = case_text(cases[1])
        
         
        all_laws = laws[:10] # 只取top10
        filter_laws = []
        for law in all_laws:
            if law not in cases[0]["laws"]:
                filter_laws.append(law)
        # print(len(filter_laws))
        relevant_laws = "\n".join([f"{i+1}. {law}" for i, law in enumerate(filter_laws)])

        judgment_content = f"""
###任务要求
根据提供的相似案件参考信息、相关法律条款和当前案件的详细认定事实，生成本案件的判决结果，包括罪名、法律条款、刑期、罚金。\n\n对判决结果要素的解释如下：1.罪名：准确判断当前案件应认定的罪名名称。2.法律条款：明确指出认定该罪名所依据的《中华人民共和国刑法》具体条款项。3.刑期：基于认定的犯罪事实，结合参考信息中相似案例及相关法律条款的量刑尺度，给出具体的刑期预测。4.罚金：根据认定的犯罪事实、参考案例的罚金数额，结合相关的法律条款，预测应判处的罚金金额，金额以“元”为单位。\n\n

###输入信息
当前案件认定事实：{query_text}\n\n
相似案件参考信息：{case1}\n\n
与本案件相关的其他法律条款：{relevant_laws}\n\n

### 输出要求
输出格式参考相似案件，请严格按照格式输出你的预测结果，仅包含指定字段，每项应当是一个列表，不要额外解释。
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
        for law_id in laws:
            law_text.append(id_to_lawtext.get(str(law_id), ""))
        result_text = "{"+f"""罪名:{crime},法律条款:{law_text},刑期:{prison},罚金:{fine}"""+"}"
        record = {"caseid":query_id,"input": judgment_content.strip(), "output": result_text}
        jsonl_file.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"Data written to {jsonl_file_path}")