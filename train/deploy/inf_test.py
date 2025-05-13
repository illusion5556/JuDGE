import json
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
import argparse
import torch
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run legal document generation with specified model suffix.')
    parser.add_argument('--suffix', type=str, required=True, help='Suffix of the model path')
    parser.add_argument('--model_path', type=str, required=True, help='Path to save the output')
    parser.add_argument('--dataset_path', type=str, default="../../data/test1.json", help='Path to the dataset')
    parser.add_argument('--output_path', type=str, default="../../output/mrag", help='Path to save the output')
    return parser.parse_args()

# Function to generate reasoning given a question
def generate_reasoning(input):
    input_content = input
    messages = [
        {"role": "system", "content": "你是一个法律助理，提供帮助。"},
        {"role": "user", "content": input_content}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=2048
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response

# Function to process a dataset
def process_dataset(dataset_path, output_path):
    # Load the dataset
    test_result = []
    with open(dataset_path, "r") as f:
        for line in tqdm(f):
            one = json.loads(line.strip())
            gen_ans = generate_reasoning(one['input'])
            exp_ans = one['output']
            # gen_ans = generate_reasoning(one['text'])
            # exp_ans = one['fd']
            print(f"Generated answer: {gen_ans}")

            # Update data and add to results list
            entry = {
                "gen_ans": gen_ans,
                "exp_ans": exp_ans
            }
            test_result.append(entry)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    args = parse_arguments()
    doc_name = args.suffix+".json"
    output_path = os.path.join(output_path,doc_name)
    # Save the results
    with open(output_path, 'w') as f:
        json.dump(test_result, f, ensure_ascii=False, indent=4)
    print(f"Results saved to {output_path}")

def main():
    args = parse_arguments()
    model_name = f"{args.model_path}{args.suffix}"

    global model, tokenizer
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    process_dataset(args.dataset_path, args.output_path)

if __name__ == "__main__":
    main()