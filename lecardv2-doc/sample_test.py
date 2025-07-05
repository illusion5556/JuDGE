import json
import random

# 读取两个JSON文件
with open('lecardv2_all.json', 'r', encoding='utf-8') as f:
    all_data = [json.loads(line) for line in f]

with open('lecardv2-doc_all.json', 'r', encoding='utf-8') as f:
    doc_data = json.load(f)

# 构建 text_id 到 CaseId 的映射字典
caseid_map = {}

for a,b in zip(all_data, doc_data):
    caseid_map[a['text_id']] = b['CaseId']

# 随机选取 500 条数据（如果总数不足则选全部）
random.seed(42)  # 可选：设置随机种子以确保结果可重复
selected_data = random.sample(all_data, min(500, len(all_data)))

# 替换 text_id 为 CaseId 并生成新数据
processed_data = []
for item in selected_data:
    text_id = item.get("text_id")
    case_id = caseid_map.get(text_id)
    
    if case_id:
        item["text_id"] = case_id  # 替换为 CaseId
        processed_data.append(item)

# 保存为新的JSON文件，每条数据一行
with open('lecardv2_test.json', 'w', encoding='utf-8') as f:
    for data in processed_data:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')

print(f"处理完成，共 {len(processed_data)} 条数据已保存至 processed_data.json")