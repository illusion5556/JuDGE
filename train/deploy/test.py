import json
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
import argparse
import torch
from difflib import SequenceMatcher
import re
import os

output_path ="../../output/inf"
test_result = []
name = "1.json"

if not os.path.exists(output_path):
    os.makedirs(output_path)
    
with open(os.path.join(output_path,name), 'w', encoding='utf-8') as f:
    json.dump(test_result, f, ensure_ascii=False, indent=4)
print(f"Results saved to {output_path}")


