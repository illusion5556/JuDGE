import json
import os

def build_exp_ans_to_id_map():
    with open('data/test.json', 'r') as infile:
        ret = {}
        for line in infile:
            data = json.loads(line.strip())
            ret[data['fd']] = data['text_id']
    
    return ret

def convert_to_jsonl(input_file, gen_output_file):
    # 读取原始数据文件
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    # 打开输出文件准备写入
    with open(gen_output_file, 'w') as gen_file:
        # 遍历数据，并将 gen_ans 重新格式化
        for idx, item in enumerate(data):
            gen_ans = item["gen_ans"]
            exp_ans = item['exp_ans']
            id = dict[exp_ans]
            print(id)

            # 构建 gen_ans 的新格式
            gen_entry = {
                "id": id,
                "document": gen_ans
            }
            # 写入到文件，每行一个 JSON 对象
            gen_file.write(json.dumps(gen_entry, ensure_ascii=False) + "\n")

def process_directory(input_dir, output_dir):
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.json'):
                input_file_path = os.path.join(root, file)
                # 构建匹配的输出路径
                relative_path = os.path.relpath(input_file_path, input_dir)
                output_file_path = os.path.join(output_dir, os.path.splitext(relative_path)[0] + '.jsonl')
                
                # 创建输出目录（如果不存在）
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                
                # 处理文件并保存到输出目录
                convert_to_jsonl(input_file_path, output_file_path)

# 使用示例
input_folder = "input"  # 输入文件夹路径
output_folder = "baseline_results"  # 输出文件夹路径

dict = build_exp_ans_to_id_map()
# print(dict)
# 处理整个目录
process_directory(input_folder, output_folder)