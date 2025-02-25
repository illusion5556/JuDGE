import random
from dataclasses import dataclass
from typing import List, Dict, Tuple
import json
import copy
import torch
from torch.utils.data import Dataset
from tqdm import tqdm
from transformers import DefaultDataCollator
from torch.nn.utils.rnn import pad_sequence
import numpy as np

IGNORE_INDEX = -100
DEFAULT_PAD_TOKEN = '[PAD]'
DEFAULT_EOS_TOKEN = '</s>'
DEFAULT_BOS_TOKEN = '<s>'
DEFAULT_UNK_TOKEN = '<unk>'

class LegalAidDataset(Dataset):
    def __init__(self, data_path,tokenizer,max_tar,max_src):

        self.max_target = max_tar
        self.max_source = max_src
        self.tokenizer = tokenizer


        self.dataset = []
        token_lengths = []  # List 
        with open(data_path, "r", encoding="utf-8") as fh:
            for i, line in tqdm(enumerate(fh)):
                item = json.loads(line.strip())  
                if not item:
                    continue 
                input_content = item['input']
                messages = [
                    {"role": "system", "content": "你是一个法律助理，提供帮助。"},
                    {"role": "user", "content": input_content}
                ]
                train_input = self.tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True  # Set to True if you want to add a generation prompt
                )
                # tokenized_input = self.tokenizer.tokenize(train_input + item['output'])
                # token_length = len(tokenized_input)
                # token_lengths.append(token_length)
                self.dataset.append(
                    {"input": train_input, "output": item["output"]})

            # # Calculate percentiles
            # percentiles = np.percentile(token_lengths, [25, 50, 75, 100, 90])
            # print(f"Top 25% length: {percentiles[0]}")
            # print(f"Median (50%) length: {percentiles[1]}")
            # print(f"Top 75% length: {percentiles[2]}")
            # print(f"Max length (100%): {percentiles[3]}")
            # print(f"Top 90% length: {percentiles[4]}")
            

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:  
        example = self.dataset[idx]
        source_txt = f"{self.tokenizer.bos_token}{example['input']}"
        tokenized_source = self.tokenizer(
            source_txt,
            max_length=self.max_source,
            truncation=True,
            add_special_tokens=False,
        )
        src_ids = tokenized_source['input_ids']

        target_txt = f"{example['output']}{self.tokenizer.eos_token}"
        tokenized_target = self.tokenizer(
            target_txt,
            max_length=self.max_source,
            truncation=True,
            add_special_tokens=False,
        )

        tgt_ids = tokenized_target['input_ids']

        if len(src_ids) + len(tgt_ids) > self.max_source:

            aaa = len(src_ids)
            bbb = len(tgt_ids)
            ccc = self.max_source

            len_src = aaa * (ccc/(aaa + bbb))
            len_src = int(len_src)

            len_tgt = bbb * (ccc/(aaa + bbb))
            len_tgt = int(len_tgt)
            # 改成从尾部截取指定长度，因为重要的信息都在尾部
            src_ids = src_ids[-len_src:]
            tgt_ids = tgt_ids[-len_tgt:]
        
        # if len(src_ids) + len(tgt_ids) > self.max_source:

        #     aaa = len(src_ids)
        #     bbb = len(tgt_ids)
        #     ccc = self.max_source

        #     len_src = aaa * (ccc/(aaa + bbb))
        #     len_src = int(len_src)

        #     len_tgt = bbb * (ccc/(aaa + bbb))
        #     len_tgt = int(len_tgt)

        #     src_ids = src_ids[0:len_src]
        #     tgt_ids = tgt_ids[0:len_tgt-1] + [tgt_ids[-1]]

        input_ids = torch.tensor(src_ids + tgt_ids)

        labels = torch.tensor(
            [-100
                for _ in range(len(src_ids))] + copy.deepcopy(tgt_ids))
        data_dict = {'input_ids': input_ids, 'labels': labels}
        return data_dict
    
class LegalAidCollator(DefaultDataCollator):
    def __init__(self, tokenizer,max_src,max_tar):
        self.max_tar = max_src
        self.max_src = max_tar
        self.tokenizer = tokenizer

    def __post_init__(self):
        super().__post_init__()
        self.rng = random.Random()

    def __call__(self, instances: List[Dict[str,
                                 torch.Tensor]]) -> Dict[str, torch.Tensor]:
        input_ids, labels = tuple([instance[key] for instance in instances]
                                  for key in ('input_ids', 'labels'))
        # print('2')

        # Pad sequences to be of equal length
        # print(f'-----------------------{self.tokenizer.pad_token_id}------------------------')
        input_ids = pad_sequence(input_ids,
                                 batch_first=True,
                                 padding_value=self.tokenizer.pad_token_id)
        labels = pad_sequence(
            labels, batch_first=True, padding_value=self.tokenizer.pad_token_id
        ) 

        # Construct attention mask based on padded input IDs
        attention_mask = input_ids.ne(self.tokenizer.pad_token_id)

        # Return collated batch as dictionary
        data_dict = {'input_ids': input_ids, 'attention_mask': attention_mask}
        if labels is not None:
            data_dict['labels'] = labels

        return data_dict
