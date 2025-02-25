from transformers import pipeline, AutoModelForCausalLM, AutoConfig, AutoTokenizer
import json
from tqdm import tqdm
import torch
def generate(model, tokenizer, input_text):
    generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
    answer = generator(input_text, max_new_tokens=2048, min_length=256, num_return_sequences=1)[0]['generated_text']
    # print('answer: ', answer)
    return answer[len(input_text):]


def process_dataset(model, tokenizer, dataset_path, output_path):
    # Load the dataset
    test_result = []
    with open(dataset_path, "r") as f:
        for line in tqdm(f):
            one = json.loads(line.strip())
            prompt = f"""
任务背景: 根据以下提供的案件事实，生成一份完整的刑法判决书。判决书需包括案件事实、法律分析、裁判理由以及最终裁判结论。
本案件事实：{one['input']}
本案件的完整判决书为：
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
    model_path = "model/hanfei"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, 
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    
    dataset_path = "/liuzyai04/thuir/yuebaoqing/casegen/data/test.json"
    output_path = "/liuzyai04/thuir/yuebaoqing/casegen/output/hanfei_ft.json"
    process_dataset(model, tokenizer, dataset_path, output_path)

