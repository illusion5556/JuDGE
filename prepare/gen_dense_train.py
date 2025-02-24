import json,random
def map_penal_corpus_to_dict(corpus): # {int: str}
    new_dict = {}
    for item in corpus:
        k, v = int(item['text_id']), item['text']
        new_dict[k] = v
    
    return new_dict
        
def get_positive_negative_examples(data, penal_corpus_dict):
    examples = []

    for entry in data:
        fact = entry["text"] # fact字段
        laws = entry["la"]
        # 收集正例内容
        positives = [penal_corpus_dict[law] for law in laws]
        # 找到所有可供选择的负例
        pos_penal_keys = laws
        non_pos_penal_keys = [key for key in penal_corpus_dict.keys() if key not in pos_penal_keys]           
        # 添加到例子列表
        for pos in positives:
            # 随机抽样负例
            negatives = []
            negatives.extend(random.sample(non_pos_penal_keys, 8))
            neg_content = []
            for ref in negatives:
                neg_content.append(penal_corpus_dict[ref])
                    
            if positives or negatives:
                examples.append({
                    'query': fact,
                    'positives': [pos],
                    'negatives': neg_content
                })
    
    return examples

def main():
    # 加载数据
    with open('../data/train.json', 'r') as f:
        train_data = [json.loads(line) for line in f]

    with open('../data/law_corpus.jsonl', 'r') as f:
        penal_corpus = [json.loads(line) for line in f]
    
    # 生成正负例
    penal_corpus_dict= map_penal_corpus_to_dict(penal_corpus)
    examples = get_positive_negative_examples(train_data, penal_corpus_dict)

    # 将结果写入文件
    with open('../retriever/train/dense_train.json', 'w') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    main()