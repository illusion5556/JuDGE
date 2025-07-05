import os
import json
import sys
sys.path.append('segment')
from segment.data_segment_xingshi import DataSegmentXingshi
from crime_extraction import get_crime
from judge_extraction import calc_time_sum, calc_amt_sum, get_time_string_from_text, get_amt_string_from_text
from law_extraction import get_penalcode_index_from_text
from tqdm import tqdm
import uuid

# 定义目标文件夹路径
folder_path = '/home/ubuntu/nas/home/dataset/LeCaRDv2-main/candidate/candidate_55192'
output_file = '/home/ubuntu/JuDGE_edit/lecardv2-doc/lecardv2-doc_all.json'
output_jsonl_file = '/home/ubuntu/JuDGE_edit/lecardv2-doc/lecardv2_all.json'

# 存放符合条件的数据
result_list = []

def extract_reasoning_n_judge(text):
    parser = DataSegmentXingshi(punctuation_replace=True)
    result = parser.parse(text)
    return result['reason'], result['judgment']

accu_file_path = '/home/ubuntu/LJP_Collection/models/new_judge_accu.txt'
accu_list = []

with open(accu_file_path, 'r', encoding='utf-8') as f:
    for line in f:
        accu = line.strip()  # 去除每行首尾的空白字符（如换行符）
        if accu:  # 如果行不为空
            accu_list.append(accu+'罪')

print(f"共读取到 {len(accu_list)} 个罪名，内容示例：{accu_list[:5]}")

# 从文件中读取法律条目并构建 law_list 列表
law_file_path = '/home/ubuntu/LJP_Collection/models/new_judge_law.txt'
law_list = []

with open(law_file_path, 'r', encoding='utf-8') as f:
    for line in f:
        law = line.strip()  # 去除每行首尾的空白字符
        if law:  # 如果行不为空
            law_list.append(law)

print(f"共读取到 {len(law_list)} 个法律条目，内容示例：{law_list[:5]}")

cnt=0
with open(output_jsonl_file, 'w', encoding='utf-8') as fout:
    # 遍历文件夹下的所有 JSON 文件

    for filename in tqdm(os.listdir(folder_path)):

        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # 提取 qw 字段
                qw = data.get('qw')
                fact = data.get('fact')
                pid = str(uuid.uuid4())

                reasoning,judgement = extract_reasoning_n_judge(qw)
                crime = get_crime(qw)
                # fine = calc_amt_sum(qw)
                fine = get_amt_string_from_text(qw)
                # pentalty = calc_time_sum(qw)
                pentalty = get_time_string_from_text(qw)
                laws = get_penalcode_index_from_text(qw)
                # print(pentalty)
                # print(fine)
                if crime == [] or laws == [] or pentalty == [] or fine == []:
                    continue
                # if reasoning and judgement and crime[0] in accu_list and pentalty != 0 and fine != 0 and laws[0] in law_list and len(qw) < 3000:
                flag = False
                for l in laws:
                    if l not in law_list:
                        flag = True
                for c in crime:
                    if c not in accu_list:
                        flag = True
                if flag:
                    continue
                if 100<len(reasoning)<512 and 100<len(judgement)<512 and len(qw)< 3000 and len(fact) < 1000:
                    dic = {}
                    dic['CaseId'] = pid
                    dic['Fact'] = fact
                    dic['Full Document'] = qw
                    dic['Reasoning'] = reasoning
                    dic['Judgement'] = judgement
                    dic['Crime Type'] = crime
                    dic['Law Articles'] = laws
                    dic['Sentence'] = pentalty
                    dic['Fine'] = fine
                    # print(dic)
                    result_list.append(dic)
                    dic_2 ={}
                    dic_2['text_id'] = str(cnt)
                    dic_2['text'] = fact
                    dic_2['la'] = [int(i) for i in laws]
                    dic_2['fd'] = qw
                    cnt+=1
                    fout.write(json.dumps(dic_2, ensure_ascii=False) + '\n')

                # else:
                #     print(filename+"不合格")
                #     print("reasoning:"+reasoning)
                #     print("judgement:"+judgement)
                #     print("crime:"+str(crime))
                #     print("laws:"+str(laws))
                #     print("pentalty:"+str(pentalty))
                #     print("fine:"+str(fine))
                # 判断是否达到 600 条
                # if len(result_list) >= 500:
                #     break

# 保存结果到新的 JSON 文件
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(result_list, f, ensure_ascii=False, indent=4)

print(f"共找到 {len(result_list)} 条符合条件的数据，已保存至 {output_file}")