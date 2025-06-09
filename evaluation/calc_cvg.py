import jieba
from bert_score import score
import json
import argparse
from nltk.translate.meteor_score import meteor_score
import sys
sys.path.append('segment')
from segment.data_segment_xingshi import DataSegmentXingshi
# 如果第一次运行，需要添加下面两行
# import nltk
# nltk.download('wordnet')

class RelevanceEvaluator:
    def __init__(self, gen_file):
        self.gen_file = gen_file
        self.results_reasoning = {
            "METEOR": [],
            "BERTScore": [],
        }
        self.results_judge = {
            "METEOR": [],
            "BERTScore": [],
        }
        self.gen_data, self.exp_data = self.load_data(gen_file)
        print(len(self.gen_data.keys()))
        print(len(self.exp_data.keys()))
        assert self.gen_data.keys() == self.exp_data.keys(), "Mismatch between gen_data and exp_data keys"

    def load_data(self, file_path):
        with open(file_path, 'r') as file:
            lines = json.load(file)
            exp_data = {}
            gen_data = {}
            for i, item in enumerate(lines):
                exp_data[i] = item['exp_ans']
                gen_data[i] = item['gen_ans']
        return gen_data, exp_data
        
    def extract_reasoning_n_judge(self, text):
        parser = DataSegmentXingshi(punctuation_replace=True)
        result = parser.parse(text)
        return result['reason'], result['judgment']

    def calculate_meteor(self, exp_text, gen_text):
        """计算 METEOR 分数"""
        reference_tokens = list(jieba.cut(exp_text))
        hypothesis_tokens = list(jieba.cut(gen_text))
        return meteor_score([reference_tokens], hypothesis_tokens)

    def calculate_metrics(self, exp_text, gen_text, results_dict):
        """通用的计算指标函数"""
        score_meteor = self.calculate_meteor(exp_text, gen_text)
        results_dict["METEOR"].append(score_meteor)

    def calc_methor(self):
        """计算 METEOR 分数"""
        for exp_idx, exp_ans in self.exp_data.items():
            gen_ans = self.gen_data[exp_idx]

            # 提取 reasoning 和 judge 部分
            exp_reasoning, exp_judge = self.extract_reasoning_n_judge(exp_ans)
            gen_reasoning = gen_ans

            # 如果任意部分提取失败，跳过这条数据
            # if not exp_reasoning or not exp_judge or not gen_reasoning or not gen_judge:
            #     continue

            # 分别计算 metrics
            self.calculate_metrics(exp_reasoning, gen_reasoning, self.results_reasoning)
            # self.calculate_metrics(exp_judge, gen_judge, self.results_judge)

    def calc_bert_score(self):
        """计算 BERTScore"""
        local_model_path = "bert-base-chinese" # 如果未下载过，会自动下载
        gen_reasoning_list, exp_reasoning_list, gen_judge_list, exp_judge_list = [], [], [], []
        for exp_idx, exp_ans in self.exp_data.items():
            gen_ans = self.gen_data[exp_idx]
            # gen_reasoning_list.append(" ".join(jieba.cut(self.extract_reasoning_n_judge(gen_ans)[0])))
            # exp_reasoning_list.append(" ".join(jieba.cut(self.extract_reasoning_n_judge(exp_ans)[0])))
            # gen_judge_list.append(" ".join(jieba.cut(self.extract_reasoning_n_judge(gen_ans)[1])))
            # exp_judge_list.append(" ".join(jieba.cut(self.extract_reasoning_n_judge(exp_ans)[1])))
            gen_reasoning = " ".join(jieba.cut(gen_ans))
            exp_reasoning = " ".join(jieba.cut(self.extract_reasoning_n_judge(exp_ans)[0]))
            

            # 截断处理
            gen_reasoning = gen_reasoning[:512]
            exp_reasoning = exp_reasoning[:512]


            gen_reasoning_list.append(gen_reasoning)
            exp_reasoning_list.append(exp_reasoning)



        
        # 计算 reasoning 的 BERTScore
        P_rsn, R_rsn, F1_rsn = score(gen_reasoning_list, exp_reasoning_list, model_type=local_model_path)
        self.results_reasoning["BERTScore"] = F1_rsn.tolist()  # 转为普通列表方便查看



    def print_results(self):
        """打印计算出的所有指标的均值"""
        print("reasoning 平均指标：")
        for metric, scores in self.results_reasoning.items():
            mean_score = sum(scores) / len(scores) if scores else 0
            print(f"{metric}: Mean = {mean_score:.4f}")

    def run(self):
        """运行整个评估流程"""
        self.calc_bert_score()
        self.calc_methor()
        self.print_results()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process a JSON file to calculate metrics.")
    parser.add_argument('--gen_file', type=str, required=True, help='Path to the input generated JSON file')
    args = parser.parse_args()

    evaluator = RelevanceEvaluator(args.gen_file)
    evaluator.run()
    print(f"This is the metrics from file {args.gen_file}!")
