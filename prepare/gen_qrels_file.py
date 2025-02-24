import json

def create_qrelsfile(data):
    qrels_lines = []
    for entry in data:
        query_id = entry['text_id']
        pos_ids = entry['la']
        # 获取正例法条ID
        for pos_id in pos_ids:
            qrels_line = f"{query_id} 0 {pos_id} 1\n"
            qrels_lines.append(qrels_line)
            
    return qrels_lines

def main():
    with open('../data/train.json', 'r') as f:
        data = [json.loads(line) for line in f]
    qrels_lines = create_qrelsfile(data)
    with open('../data/qrels_file_train', 'w') as f:
        for line in qrels_lines:
            f.write(line)
    
    with open('../data/test.json', 'r') as f:
        data = [json.loads(line) for line in f]
    qrels_lines = create_qrelsfile(data)
    with open('../data/qrels_file_test', 'w') as f:
        for line in qrels_lines:
            f.write(line)

if __name__ == "__main__":
    main()