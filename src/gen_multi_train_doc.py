# 创建多路检索方法的训练数据集
import json
from difflib import SequenceMatcher

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

# 读取 law-corpus.jsonl 文件，构建 text_id 到 text 的映射
def build_law_id_text_mapping(law_corpus_path):
    id_to_text = {}
    with open(law_corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            text_id = str(item['text_id'])
            name_n_text = f"{item['name']}：{item['text']}"
            id_to_text[text_id] = name_n_text
    return id_to_text

# 读取 case_corpus.jsonl 文件，构建 text_id 到 text 的映射
def build_case_id_text_mapping(case_corpus_path):
    id_to_text = {}
    with open(case_corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            text_id = item['text_id']
            text = item['text']
            qw = item['fd']
            id_to_text[text_id] = (text, qw)

    return id_to_text

# 解析 runfile 并根据编号找到对应的 text 内容
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

# 解析 runfile 并根据编号找到对应的 text 内容
def extract_case_texts(runfile_path, case_corpus_path, queryID_to_text):
    id_to_text = build_case_id_text_mapping(case_corpus_path)
    query_to_qws = {}
    
    with open(runfile_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            query_id = parts[0]
            case_id = parts[2]
            case_text, qw = id_to_text[case_id]
            
            query = queryID_to_text[query_id]
            if are_strings_similar(query, case_text):
                continue

            if query_id not in query_to_qws:
                query_to_qws[query_id] = []
            
            query_to_qws[query_id].append(qw)
    
    return query_to_qws

# 示例调用
query_path = '../data/train.json'
queryId_to_text = build_query_id_text_mapping(query_path)
queryId_to_qw = build_query_id_qw_mapping(query_path)

law_runfile_path = '../reranker/score/train/reranker_run_file_train'  # 替换为实际路径
law_corpus_path = '../data/law_corpus.jsonl'  # 替换为实际路径

case_runfile_path = '../retriever/encode/sailer/run_file_train'  # 替换为实际路径
case_corpus_path = '../data/case_corpus.jsonl'

ljp_result_path = '/home/ubuntu/JuDGE_edit/train/train_ljp.json' 

# law_result = extract_law_texts(law_runfile_path, law_corpus_path)
qw_result = extract_case_texts(case_runfile_path, case_corpus_path, queryId_to_text)
ljp_result = {}
with open(ljp_result_path, 'r') as f1, open(query_path, 'r') as f2:
    ids=[]
    for line in f2:
        item = json.loads(line)
        ids.append(item['text_id'])
    idx = 0
    for item in f1: 
        item = json.loads(item)
        ljp_result[ids[idx]] = item['output']
        idx += 1

jsonl_file_path = '../train/train_doc.json'
with open(jsonl_file_path, 'w') as jsonl_file:
    for query_id, ljp in ljp_result.items():
        query_text = queryId_to_text[query_id]
        qws = qw_result[query_id]

        relevant_qw = "无相关判决书"
        # 找出所有符合长度要求的 qw
        suitable_qw = [qw for qw in qws if len(qw) <= 1500]
        
        if suitable_qw:
            relevant_qw = f"相关案例判决书：{suitable_qw[0]}"
        else:
            # 如果没有符合长度要求的 qw，则找出最短的那个
            shortest_qw = min(qws, key=len)
            relevant_qw = f"相关案例判决书：{shortest_qw}"  


        judgment_content = f"""
任务背景: 根据以下提供的相关案例、法律条款和案件事实，生成一份完整的刑法判决书。判决书需包括案件事实、法律分析、裁判理由以及最终裁判结论。\n\n判决书的格式方面，请参考相关案例中的格式。
{relevant_qw}

以下是本案的初步裁判结论：
{ljp}
请根据以上内容和下面的案件事实描述，为这个案件生成一份刑事判决书，结构完整，参考提供给你的判决书的格式（需包含案件事实陈述、法律分析、裁判理由及裁判结论等部分。不超过两千字。
本案件事实：{query_text}
本案件的完整判决书为：
"""
        # print("输入：", judgment_content)
        # print('-'* 100)
        # 将判决书内容写入 JSONL 文件
        record = {"input": judgment_content.strip(), "output": queryId_to_qw[query_id]}
        jsonl_file.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"Data written to {jsonl_file_path}")