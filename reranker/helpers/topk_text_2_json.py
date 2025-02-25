# Copyright 2021 Reranker Author. All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

from transformers import AutoTokenizer
from argparse import ArgumentParser
from tqdm import tqdm
from multiprocessing import Pool
import json
from collections import defaultdict

parser = ArgumentParser()

parser.add_argument('--save_to', required=True)
parser.add_argument('--tokenizer', required=True)
parser.add_argument('--generate_id_to')
parser.add_argument('--truncate', type=int, default=512)
parser.add_argument('--q_truncate', type=int, default=16)
parser.add_argument('--qry_train_file', required=True)
parser.add_argument('--law_data_file', required=True)
parser.add_argument('--run_file_train', required=True)
args = parser.parse_args()

tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, use_fast=True)

law_data, qry_train_data = [], []
with open(args.qry_train_file, 'r') as f1, open(args.law_data_file, 'r') as f2:
    for l1 in f1:
        tmp = json.loads(l1.strip())
        qry_train_data.append(tmp)
    for l2 in f2:
        tmp = json.loads(l2.strip())
        law_data.append(tmp)
        
did_2_body = {int(x['text_id']):x['text'] for x in law_data}
qid_2_body = {int(x['text_id']):x['text'] for x in qry_train_data}
  
rankings = defaultdict(list)
with open(args.run_file_train) as f: 
    for l in f: # 对于rank_file中的每一行：
        qid, _, pid, _, _ = l.split()
        rankings[qid].append(pid)
    
with open(args.save_to, 'w') as jfile:
    all_ids = []

    # Iterate over the dataset and process each item sequentially
    for data_item in tqdm(qry_train_data):
        qry_id = data_item['text_id']
        q_body = data_item['text']
        pids = rankings[qry_id]
        for pid in pids:
            all_ids.append((qry_id, pid))
            
            p_body = did_2_body[pid]
            qry_encoded = tokenizer.encode(
                q_body,
                truncation=True if args.q_truncate else False,
                max_length=args.q_truncate,
                add_special_tokens=False,
                padding=False,
            )
            doc_encoded = tokenizer.encode(
                p_body,
                truncation=True,
                max_length=args.truncate,
                add_special_tokens=False,
                padding=False
            )
            entry = {
                'qid': qid,
                'pid': pid,
                'qry': qry_encoded,
                'psg': doc_encoded,
            }
            entry = json.dumps(entry)
            jfile.write(entry + '\n')
            
        

    if args.generate_id_to is not None:
        with open(args.generate_id_to, 'w') as id_file:
            for qry_id, doc_id in all_ids:
                id_file.write(f'{qry_id}\t{doc_id}\n')

