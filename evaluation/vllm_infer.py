import json
from vllm import LLM, SamplingParams
import torch
import time
from datetime import datetime
from tqdm import tqdm

input_file = "/home/ubuntu/JuDGE_edit/train/test_multi.json"
# 1. 配置参数
CONFIG = {
    "model": "/home/ubuntu/weight/wubinglin/Qwen2.5-72B-Instruct-AWQ",
    "quantization": "awq",
    "tensor_parallel_size": 8,
    "max_model_len": 8192,
    "output_file": f"awq_mrag.json"
}

MAX_BATCH_SIZE = 501

# 2. 采样参数设置
SAMPLING_PARAMS = SamplingParams(
    temperature=0.1,
    top_p=1,
    max_tokens=3000,
    stop_token_ids=[151643]  # Qwen特殊终止符
)

BATCH_INPUTS = []
with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        item = json.loads(line)
        BATCH_INPUTS.append(item)

# BATCH_INPUTS = BATCH_INPUTS[:200]
def run_batch_inference():
    # 初始化模型
    llm = LLM(
        model=CONFIG["model"],
        quantization=CONFIG["quantization"],
        tensor_parallel_size=CONFIG["tensor_parallel_size"],
        max_model_len=CONFIG["max_model_len"],
        trust_remote_code=True,
        gpu_memory_utilization=0.7,
        max_num_seqs=128
    )
    tokenizer = llm.get_tokenizer()

    # 收集结果
    results = []
    # 执行推理
    for i in tqdm(range(0, len(BATCH_INPUTS), MAX_BATCH_SIZE)):
        batch = BATCH_INPUTS[i:i+MAX_BATCH_SIZE]

        
        # 执行推理
        outputs = llm.generate([item["input"] for item in batch], SAMPLING_PARAMS)
        
        # 收集结果
        # for out in outputs:
        #     results.append(out.outputs[0].text)
        
        for i, out in enumerate(outputs):
        
            result = {
                "prompt": BATCH_INPUTS[i]["input"],
                "gen_ans": out.outputs[0].text,
                "exp_ans": BATCH_INPUTS[i]["output"], 
            }
            results.append(result)
        # 显存清理
        torch.cuda.empty_cache()
    


    with open(CONFIG["output_file"], 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)




if __name__ == "__main__":
    print("🚀 开始Qwen2.5-72B-AWQ批量推理...")
    run_batch_inference()
    