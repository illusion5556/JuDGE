'''
Author: lihaitao
Date: 2023-05-20 15:06:50
LastEditors: Do not edit
LastEditTime: 2023-05-20 19:32:43
'''
from transformers import AutoModel
import torch
import os
os.environ["CUDA_VISIBLE_DEVICES"] = '2'
import sys
sys.path.append("../src") 
from modeling_chatglm import ChatGLMForConditionalGeneration
from tokenization_chatglm import ChatGLMTokenizer
from tqdm import tqdm
from peft import PeftModel
import argparse, json

def generate(model, tokenizer, text):
    with torch.no_grad():
        input_text = text
        ids = tokenizer.encode(input_text)
        input_ids = torch.LongTensor([ids]).cuda()
        output = model.generate(
            input_ids=input_ids,
            max_new_tokens=2048,
            do_sample=False,
            temperature=0.7,
            num_return_sequences=1
        )[0]
        output = tokenizer.decode(output)
        answer = output[len(input_text):]
    return answer.strip()
    
def process_dataset(model, tokenizer, dataset_path, output_path):
    # Load the dataset
    test_result = []
    with open(dataset_path, "r") as f:
        for line in tqdm(f):
            one = json.loads(line.strip())
            prompt = f"""
案件事实：{one['input']}
请根据上面提供的事实描述，生成一篇完整且具有法律效力的中文的刑事判决书。生成的文书必须结构严谨、逻辑清晰；确保文书所有部分均符合真实司法文书的写作规范，语言应正式、客观、清晰
"""
            gen_ans = generate(model, tokenizer, prompt)
            exp_ans = one['output']
            print(f"Generated answer: {gen_ans}")

            # Update data and add to results list
            entry = {
                "gen_ans": gen_ans,
                "exp_ans": exp_ans
            }
            test_result.append(entry)

    # Save the results
    with open(output_path, 'w', encoding="utf-8") as f:
        json.dump(test_result, f, ensure_ascii=False, indent=4)
    print(f"Results saved to {output_path}")
    
    
if __name__ == "__main__":
    model_name = "../model/LexiLaw"
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--base_model", type=str, default=model_name)
    argparser.add_argument("--interactive", default=True)

    args = argparser.parse_args()

    model = ChatGLMForConditionalGeneration.from_pretrained(args.base_model, trust_remote_code=True)
    tokenizer = ChatGLMTokenizer.from_pretrained(model_name, trust_remote_code=True)
    
    torch.set_default_tensor_type(torch.cuda.FloatTensor)
    model = model.eval()
    model.half().cuda()
    
    dataset_path = "/liuzyai04/thuir/yuebaoqing/casegen/data/test.json"
    output_path = "/liuzyai04/thuir/yuebaoqing/casegen/output/lexilaw-new.json"
    process_dataset(model, tokenizer, dataset_path, output_path)

