# 此代码用于生成case_corpus，后续用于dense retriver的encode
import json

def modify_jsonl_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        data = json.load(infile)
        for idx, item in enumerate(data):  # 行号从1开始
            try:
                record = {
                    'text_id': item['CaseId'],
                    'text': item['Fact'],
                    'fd': item['Full Document']
                }
                
                # 将修改后的记录写出到新文件中
                json_record = json.dumps(record, ensure_ascii=False)
                outfile.write(json_record + '\n')

            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line at line {idx}")

# 使用函数来处理指定的输入和输出文件名
input_filename = '../data/all.json'
output_filename = '../data/case_corpus.jsonl'
modify_jsonl_file(input_filename, output_filename)