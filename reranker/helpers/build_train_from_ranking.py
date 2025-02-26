# Copyright 2021 Reranker Author. All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
from argparse import ArgumentParser
from transformers import AutoTokenizer
import json
import os
from collections import defaultdict
import datasets
import random
from tqdm import tqdm

parser = ArgumentParser()
parser.add_argument('--tokenizer_name', required=True)

parser.add_argument('--truncate', type=int, default=200)
parser.add_argument('--q_truncate', type=int, default=512)
parser.add_argument('--sample_from_top', type=int, default=100)
parser.add_argument('--n_sample', type=int, default=10)
parser.add_argument('--random', action='store_true')

parser.add_argument('--run_file_train', required=True)
parser.add_argument('--output_train_file', required=True)
parser.add_argument('--qry_train_file', required=True)
parser.add_argument('--law_data_file', required=True)
args = parser.parse_args()


def read_qrel(): # 将query和相关的doc存储成dict的形式，形式为 qid: [docid1, docid2, ...]
    qrel = {}
    with open(args.qry_train_file, 'r') as f:
        for line in f:
            content = json.loads(line.strip())
            qid = content['text_id']
            qrel[qid] = content['la']
    
    return qrel

qrel = read_qrel()
rankings = defaultdict(list)
no_judge = set()

with open(args.run_file_train) as f: 
    for l in f: # 对于rank_file中的每一行：
        qid, _, pid, _, _, _ = l.split()
        if qid not in qrel: # 如果query没有对应的相关doc，则添加到no_judge中
            no_judge.add(qid)
            continue
        if int(pid) in qrel[qid]:  # relevant
            continue
        # 将事实上不相关但是在rank_file中的doc添加到query的rankings映射list中
        rankings[qid].append(int(pid))

print(f'{len(no_judge)} queries not judged and skipped', flush=True)

law_data, qry_train_data = [], []
with open(args.qry_train_file, 'r') as f1, open(args.law_data_file, 'r') as f2:
    for l1 in f1:
        tmp = json.loads(l1.strip())
        qry_train_data.append(tmp)
    for l2 in f2:
        tmp = json.loads(l2.strip())
        law_data.append(tmp)  
    
did_2_body = {int(x['text_id']):x['text'] for x in law_data}
qid_2_body = {x['text_id']:x['text'] for x in qry_train_data}

tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_name, use_fast=True)

queries = list(rankings.keys()) # 所有的queries的list

with open(args.output_train_file, 'w') as f:
    for qid in tqdm(queries): # 对每个query：
        # pick from top of the full initial ranking
        negs = rankings[qid][:args.sample_from_top]  # 找到query对应的rankings的前100个，即不相关但是出现在了rank_file中
        # shuffle if random flag is on
        if args.random:
            random.shuffle(negs)
        # pick n samples
        negs = negs[:args.n_sample] # 选10个负例

        neg_encoded = []
        for neg in negs:
            body = did_2_body[neg]
            encoded_neg = tokenizer.encode(
                body,
                add_special_tokens=False,
                max_length=args.truncate,
                truncation=True
            )
            neg_encoded.append({
                'passage': encoded_neg,
                'pid': str(neg),
            })

        pos_encoded = []
        for pos in qrel[qid]:
            body = did_2_body[pos]
            encoded_pos = tokenizer.encode(
                body,
                add_special_tokens=False,
                max_length=args.truncate,
                truncation=True
            )
            pos_encoded.append({
                'passage': encoded_pos,
                'pid': str(pos),
            })

        q_body = qid_2_body[qid]
        query_dict = {
            'qid': qid,
            'query': tokenizer.encode(
                q_body,
                add_special_tokens=False,
                max_length=args.q_truncate,
                truncation=True),
        }
        item_set = {
            'qry': query_dict,
            'pos': pos_encoded,
            'neg': neg_encoded,
        }
        f.write(json.dumps(item_set) + '\n')

print("DONE!")