import json

def convert_to_jsonl(input_file, gen_output_file, exp_output_file):
    # 读取原始数据文件
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    # 打开输出文件准备写入
    with open(gen_output_file, 'w') as gen_file, open(exp_output_file, 'w') as exp_file:
        # 遍历数据，并将 gen_ans 和 exp_ans 重新格式化
        for idx, item in enumerate(data):
            gen_ans = item["gen_ans"]
            exp_ans = item["exp_ans"]

            # 构建 gen_ans 和 exp_ans 的新格式
            gen_entry = {
                "id": idx,
                "document": gen_ans
            }
            exp_entry = {
                "id": idx,
                "document": exp_ans
            }

            # 写入到文件，每行一个 JSON 对象
            gen_file.write(json.dumps(gen_entry, ensure_ascii=False) + "\n")
            exp_file.write(json.dumps(exp_entry, ensure_ascii=False) + "\n")


# 使用示例
input_file = "sample.json"  # 输入文件名，原始格式
gen_output_file = "generated.jsonl"  # 输出文件名（gen_ans）
exp_output_file = "expected.jsonl"  # 输出文件名（exp_ans）

# 转换并写入到 gen_output.jsonl 和 exp_output.jsonl
convert_to_jsonl(input_file, gen_output_file, exp_output_file)
