# Copyright 2021 Reranker Author. All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('--score_file', required=True)
parser.add_argument('--reranker_run_file', required=True)
parser.add_argument('--part', required=True)
args = parser.parse_args()

run_id = f"lr_reranker_{args.part}"
with open(args.score_file) as f:
    lines = f.readlines()

all_scores = defaultdict(dict)

for line in lines:
    if len(line.strip()) == 0:
        continue
    qid, did, score = line.strip().split()
    score = float(score)
    all_scores[qid][did] = score

qq = list(all_scores.keys())

with open(args.reranker_run_file, 'w') as f:
    for qid in qq:
        score_list = sorted(list(all_scores[qid].items()), key=lambda x: x[1], reverse=True)
        for rank, (did, score) in enumerate(score_list):
            f.write(f'{qid}\t0\t{did}\t{rank+1}\t{score}\t{run_id}\n')

