import json
import argparse
from crime_extraction import process_special_case
from judge_extraction import get_time_string_from_text, calc_amt_sum
# from law_extraction import get_penalcode_index_from_text
import re
import chinese2digits as c2d




def parse_crime(text):
    # 匹配 罪名: [...] 部分
    pattern = r"罪名:(\[.*?\]),"
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        try:
            # 将字符串转换为 Python 对象
            crime_list = json.loads(match.group(1).replace("'", '"'))
            return crime_list
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误: {e}")
            return []
    else:
        print("未找到罪名字段")
        return []


def parse_prison(text):
    # 匹配 刑期: [...] 部分
    pattern = r"刑期:(\[.*?\]),"
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        try:
            # 将字符串转换为 Python 列表
            prison_list = json.loads(match.group(1).replace("'", '"'))
            return prison_list
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误: {e}")
            return []
    else:
        print("未找到刑期字段")
        return []


def parse_laws(text):
    # 匹配 法律条款: [...] 部分
    pattern = r"法律条款:(\[.*?\]),"
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        try:
            # 将字符串转换为 Python 列表
            laws_list = json.loads(match.group(1).replace("'", '"'))
            return laws_list
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误: {e}")
            return []
    else:
        print("未找到法律条款字段")
        return []


def parse_fine(text):
    # 匹配 罚款: [...] 部分
    pattern = r"罚金:(\[.*?\])"
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        try:
            # 将字符串转换为 Python 列表
            fine_list = json.loads(match.group(1).replace("'", '"'))
            return fine_list
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误: {e}")
            return []
    else:
        print("未找到罚款字段")
        return []

def get_crime(raw_list):
    raw_list = set(raw_list)
    raw_labels = set(map(process_special_case, raw_list))
    # print(raw_labels)
    # 如果有 ''，说明遇到了无法识别的罪名
    # 如有需要可根据这类情况查看具体的文书内容
    if '' in raw_labels: raw_labels.remove('')
    # print(raw_labels)
    return raw_labels

def get_penalcode_index_from_text(doc): # 这里是一个简化了的处理方法，匹配所有“第xxx条”并转换成阿拉伯数字
    # pattern = r"[》、]第[一二三四五六七八九零十百]条"
    doc = "。".join(doc)
    pattern = r"第[一二三四五六七八九零十百]+条"
    matches = re.findall(pattern, doc)
    ret = []
    for match in matches:
        try:
            # 尝试转换中文数字为阿拉伯数字
            converted_list = c2d.takeNumberFromString(match)['digitsStringList']
            assert len(converted_list) == 1
            ret.append(converted_list[0])
        except Exception as e:
            print(f"跳过不符合格式的匹配: {match}, 错误: {e}")
            pass 
            # 如果转换失败，自动跳过
            
    ret = list(set(ret))
    return ret

def get_time_from_text(doc):
    # print('-' * 80)
    full_doc = doc
    ret = get_time_string_from_text(doc)
    if len(ret) == 0:
        ret = get_time_string_from_text(full_doc)
    
    ret = list(set(ret))
    # print(ret)
    return ret
def calc_time_sum(doc):
    all_judge_time_str = get_time_from_text(doc)
    if len(all_judge_time_str) == 0: # 如果没有提取到刑期长度
        return -1
    
    time_sum = 0
    for judge_time_str in all_judge_time_str:
        num_list = c2d.takeNumberFromString(judge_time_str)['digitsStringList']
        num = 0
        if len(num_list) == 2:
            if '年' in judge_time_str and '月' in judge_time_str: # 如果是x年x月的格式
                num = int(num_list[0]) * 12 + int(num_list[1])
            else:
                print('发生错误：', judge_time_str)
                num = int(num_list[0]) # 取第一个
        elif len(num_list) == 1:
            if '年' in judge_time_str:
                num = int(num_list[0]) * 12
            elif '月' in judge_time_str:
                num = int(num_list[0])
        elif len(num_list) == 0:
            if '无期徒刑' in judge_time_str:
                num = 240
            elif '死刑' in judge_time_str:
                num = 10001 # 一会儿只需检查是否返回的数额大于10000，即可知道是否出现死刑了
            else:
                num = 0
        else:
            print('有不合规范的刑期长度：', judge_time_str)
        
        time_sum += num
    # print(time_sum)
    return time_sum

class MetricsCalculator:
    def __init__(self, gen_file):
        self.gen_file = gen_file
        self.gen_data, self.exp_data = self.load_data(gen_file)


        
        # Initialize counters for metrics
        self.total_crime_rec = self.total_crime_prec = 0
        self.total_time_score = self.total_amount_score = 0
        self.total_penalcode_index_rec = self.total_penalcode_index_prec = 0
        self.time_num = self.amount_num = 0

        assert self.gen_data.keys() == self.exp_data.keys(), "Mismatch between gen_data and exp_data keys"
        self.n = len(self.exp_data)  # Total number of items in data

    def load_data(self, file_path):
        with open(file_path, 'r') as file:
            lines = json.load(file)
            exp_data = {}
            gen_data = {}
            for i, item in enumerate(lines):
                exp_data[i] = item['exp_ans']
                gen_data[i] = item['gen_ans']
        return gen_data, exp_data
    


    def get_all_from_text(self, text): 
        crime = get_crime(parse_crime(text))
        prison = calc_time_sum('。'.join(parse_prison(text)))
        fine = calc_amt_sum('。'.join(parse_fine(text)))
        laws = get_penalcode_index_from_text(parse_laws(text))


        return crime, prison, fine, laws

    def calculate_recall_and_precision(self, expected, actual):
        expected_set = set(expected)
        actual_set = set(actual)
        true_positive = len(expected_set & actual_set)

        recall = true_positive / len(expected_set) if len(expected_set) > 0 else 0
        precision = true_positive / len(actual_set) if len(actual_set) > 0 else 0

        return recall, precision

    def calculate_percent_for_judge(self, exp_val, act_val):
        if exp_val == act_val == 0:
            return 1.0
        if (exp_val >= 0 and act_val) < 0 or (exp_val < 0 and act_val >= 0):  # Different signs
            return 0.0
        if (exp_val - 10000) * (act_val - 10000) < 0:  # Both must either have or lack the death penalty
            return 0.0
        x = abs(exp_val - act_val) / max(exp_val, act_val)
        y = 1 - x
        return y

    def calc_metrics(self):
        for exp_id, exp_ans in self.exp_data.items():
            gen_ans = self.gen_data[exp_id]

            exp_crime, exp_time, exp_amount, exp_penalcode_index = self.get_all_from_text(exp_ans)
            gen_crime, gen_time, gen_amount, gen_penalcode_index = self.get_all_from_text(gen_ans)

            crime_rec, crime_prec = self.calculate_recall_and_precision(exp_crime, gen_crime)
            penalcode_index_rec, penalcode_index_prec = self.calculate_recall_and_precision(exp_penalcode_index, gen_penalcode_index)

            # Accumulate the results
            self.total_crime_rec += crime_rec
            self.total_crime_prec += crime_prec
            self.total_penalcode_index_rec += penalcode_index_rec
            self.total_penalcode_index_prec += penalcode_index_prec

            if exp_time >= 0 or gen_time >= 0:
                time_score = self.calculate_percent_for_judge(exp_time, gen_time)
                self.total_time_score += time_score
                self.time_num += 1

            if exp_amount >= 0 or gen_amount >= 0:
                amount_score = self.calculate_percent_for_judge(exp_amount, gen_amount)
                self.total_amount_score += amount_score
                self.amount_num += 1

    def print_results(self):
        avg_crime_rec = self.total_crime_rec / self.n
        avg_crime_prec = self.total_crime_prec / self.n
        avg_penalcode_index_rec = self.total_penalcode_index_rec / self.n
        avg_penalcode_index_prec = self.total_penalcode_index_prec / self.n

        # Calculate F1 scores
        f1_crime = 2 * (avg_crime_prec * avg_crime_rec) / (avg_crime_prec + avg_crime_rec) if (avg_crime_prec + avg_crime_rec) != 0 else 0
        f1_penalcode_index = 2 * (avg_penalcode_index_prec * avg_penalcode_index_rec) / (avg_penalcode_index_prec + avg_penalcode_index_rec) if (avg_penalcode_index_prec + avg_penalcode_index_rec) != 0 else 0

        # Calculate average judge time score and average amount score
        avg_time_score = self.total_time_score / self.time_num if self.time_num > 0 else 0
        avg_amount_score = self.total_amount_score / self.amount_num if self.amount_num > 0 else 0

        # Print the results
        print(f"Average Judge Time Score: {avg_time_score:.4f}, Average Amount Score: {avg_amount_score:.4f}")
        print(f"Average Crime Recall: {avg_crime_rec:.4f}, Average Crime Precision: {avg_crime_prec:.4f}, F1 Score: {f1_crime:.4f}")
        print(f"Average Penalcode Index Recall: {avg_penalcode_index_rec:.4f}, Average Penalcode Index Precision: {avg_penalcode_index_prec:.4f}, F1 Score: {f1_penalcode_index:.4f}")
        print(self.time_num, self.amount_num)


def main():
    parser = argparse.ArgumentParser(description="Process a JSON file to calculate metrics.")
    parser.add_argument('--gen_file', type=str, required=True, help='Path to the input generated JSON file')
    args = parser.parse_args()

    # Create an instance of MetricsCalculator
    calculator = MetricsCalculator(args.gen_file)
    
    # Calculate the metrics
    calculator.calc_metrics()
    
    # Print the results
    calculator.print_results()
    print(f"This is the metrics from file {args.gen_file}!")


if __name__ == "__main__":
    main()
