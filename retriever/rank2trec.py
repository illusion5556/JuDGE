import argparse

def process_file(input_file, output_file, model_name, part):
    # 打开原始文件和新文件
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        current_qid = None
        rank = 0

        # 逐行读取文件
        for line in infile:
            qid, pid, score = line.strip().split()

            # 如果是新查询的开始，重置排名
            if qid != current_qid:
                current_qid = qid
                rank = 1
            else:
                rank += 1

            # 生成新格式的行
            new_line = f"{qid} 0 {pid} {rank} {score} {model_name}_{part}\n"

            # 写入新文件
            outfile.write(new_line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--rank_txt_file', type=str, required=True)
    parser.add_argument('--run_file', type=str, required=True)
    parser.add_argument('--model_name', type=str, required=True)
    parser.add_argument('--part', type=str, required=True)
    args = parser.parse_args()
    input_file_path = args.rank_txt_file
    output_file_path = args.run_file
    model_name = args.model_name
    part = args.part

    process_file(input_file_path, output_file_path, model_name, part)