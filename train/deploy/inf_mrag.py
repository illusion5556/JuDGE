import json
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
import argparse
import torch
from difflib import SequenceMatcher
import re

# 固定的参数
MODEL_BASE_PATH = "/liuzyai04/thuir/yuebaoqing/casegen/model/multi/"

# 解析命令行参数
def parse_arguments():
    parser = argparse.ArgumentParser(description='Run legal document generation with specified model suffix.')
    parser.add_argument('--suffix', type=str, required=True, help='Suffix of the model path')
    parser.add_argument('--output_path', type=str, required=True, help='Path to save the output')
    return parser.parse_args()

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
            text_id = str(item['text_id'])
            text = item['text']
            id_to_text[text_id] = text
    return id_to_text

# 读取 queries_train.json 文件，构建 text_id 到 qw 的映射
def build_query_id_qw_mapping(query_path):
    id_to_qw = {}
    with open(query_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            text_id = str(item['text_id'])
            qw = item['qw']
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
            text_id = str(item['text_id'])
            text = item['text']
            qw = item['qw']
            id_to_text[text_id] = (text, qw)
    return id_to_text

# 解析 runfile 并根据编号找到对应的 text 内容
def extract_law_texts(runfile_path, law_corpus_path):
    id_to_text = build_law_id_text_mapping(law_corpus_path)
    query_to_laws = {}
    
    with open(runfile_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
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
    query_to_cases = {}
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
            
            if query_id not in query_to_cases:
                query_to_cases[query_id] = []
            if query_id not in query_to_qws:
                query_to_qws[query_id] = []
            
            query_to_cases[query_id].append(case_text)
            query_to_qws[query_id].append(qw)
    
    return query_to_cases, query_to_qws

def generate_reasoning(fact, relevant_cases, relevant_qw, relevant_laws, jsonl_path='log.jsonl'):
    input_content = f"""
任务背景: 根据以下提供的相关案例、法律条款和案件事实，生成一份完整的刑法判决书。判决书需包括案件事实、法律分析、裁判理由以及最终裁判结论。\n\n判决书的格式方面，请参考相关案例中的格式。
{relevant_qw}

以下是与本案件相关的法律条款：
{relevant_laws}
请根据以上内容和下面的案件事实描述，为这个案件生成一份刑事判决书，结构完整，参考提供给你的判决书的格式（需包含案件事实陈述、法律分析、裁判理由及裁判结论等部分。不超过两千字。
本案件事实：{fact}
本案件的完整判决书为：
"""
    # log_data = {"input_content": input_content}
    # with open(jsonl_path, 'a', encoding='utf-8') as f:
    #     f.write(json.dumps(log_data, ensure_ascii=False) + "\n")
    print(input_content)

    messages = [
        {"role": "system", "content": "你是一个法律助理，提供帮助。"},
        {"role": "user", "content": input_content}
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=2048
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response

# 处理数据集
def process_dataset(dataset_path, output_path, case_result, qw_result, law_result):
    test_result = []
    with open(dataset_path, "r", encoding="utf-8") as f:
        for query_id, line in tqdm(enumerate(f), desc="Processing dataset"):
            one = json.loads(line.strip())
            # query_id = str(one['query_id'])
            query_id = str(query_id)
            
            cases = case_result.get(query_id, [])
            qws = qw_result[query_id]
            
            relevant_cases = f"相关案例：{cases[0]}" if cases else "相关案例：无相关案例"
            
            relevant_qw = "无相关判决书"
            # 找出所有符合长度要求的 qw
            suitable_qw = [qw for qw in qws if len(qw) <= 2048]
            
            if suitable_qw:
                relevant_qw = f"相关案例判决书：{suitable_qw[0]}"
            else:
                # 如果没有符合长度要求的 qw，则找出最短的那个
                shortest_qw = min(qws, key=len)
                relevant_qw = f"相关案例判决书：{shortest_qw}"  
            
            laws = law_result.get(query_id, [])
            relevant_laws = "\n".join([f"{i+1}. {law}" for i, law in enumerate(laws[:10])])
            
            fact = one['input']
            exp_ans = one['output']
            
            gen_ans = generate_reasoning(fact, relevant_cases, relevant_qw, relevant_laws)
            print(f"Generated answer: {gen_ans}")
            
            entry = {
                "gen_ans": gen_ans,
                "exp_ans": exp_ans
            }
            test_result.append(entry)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(test_result, f, ensure_ascii=False, indent=4)
    print(f"Results saved to {output_path}")

# 主函数
def main():
    args = parse_arguments()
    model_name = f"{MODEL_BASE_PATH}{args.suffix}"
    
    # 示例调用
    query_path = '../data/queries.json'
    queryId_to_text = build_query_id_text_mapping(query_path)
    queryId_to_qw = build_query_id_qw_mapping(query_path)

    law_runfile_path = '../dense_result/LR/run_file'  # 替换为实际路径
    law_corpus_path = '../data/law_corpus.json'  # 替换为实际路径

    case_runfile_path = '../dense_result/sailer/run_file'  # 替换为实际路径
    case_corpus_path = '../data/case_corpus.json'

    law_result = extract_law_texts(law_runfile_path, law_corpus_path)
    case_result, qw_result = extract_case_texts(case_runfile_path, case_corpus_path, queryId_to_text)

    global model, tokenizer
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    dataset_path = "../data/test.json"
    process_dataset(dataset_path, args.output_path, case_result, qw_result, law_result)

if __name__ == "__main__":
    main()
