from transformers import pipeline, AutoModelForCausalLM, AutoConfig, AutoTokenizer
import json, torch
from tqdm import tqdm
def generate(model, tokenizer, input_text):
    generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
    answer = generator(input_text, max_new_tokens=2048, min_length=256, num_return_sequences=1)[0]['generated_text']
    return answer[len(input_text):]


def process_dataset(model, tokenizer, dataset_path, output_path):
    # Load the dataset
    test_result = []
    with open(dataset_path, "r") as f:
        for line in tqdm(f):
            one = json.loads(line.strip())
            prompt = f"""
案件事实：{one['input']}
请根据上面提供的事实描述，生成一篇完整且具有法律效力的中文的刑事判决书。生成的文书必须结构严谨、逻辑清晰；确保文书所有部分均符合真实司法文书的写作规范，语言应正式、客观、清晰。判决书格式请参照下面的示例：
示例：
刑法判决书:  
北京市丰台区人民法院 刑事判决书 被告人程诚，男，1987年7月1日出生于北京市，汉族，初中文化，无业。北京市丰台区人民检察院以京丰检一部刑诉（2019）1394号起诉书指控被告人程诚犯诈骗罪，于2019年10月18日向本院提起公诉。本院依法组成合议庭，适用简易程序，公开开庭审理了本案。北京市丰台区人民检察院指控被告人程诚犯诈骗罪的事实清楚，证据确实、充分，罪名成立。鉴于被告人程诚自动投案，如实供述自己的罪行，系自首，且自愿认罪认罚，本院依法对其从轻处罚。依照《中华人民共和国刑法》第二百六十六条、第六十七条第一款、第五十二条、第六十一条、第五十三条、第六十四条之规定，判决如下： 被告人程诚犯诈骗罪，判处有期徒刑五年，并处罚金人民币五万元。

请参考以上示例，根据案件事实生成一份刑事判决书，结构完整，需包含案件事实陈述、法律分析、裁判理由及裁判结论等部分。不超过两千字。
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
    model_path = "../LLM/hanfei"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    
    dataset_path = "/liuzyai04/thuir/yuebaoqing/casegen/data/test.json"
    output_path = "/liuzyai04/thuir/yuebaoqing/casegen/output/hanfei_fs-new2.json"
    process_dataset(model, tokenizer, dataset_path, output_path)

