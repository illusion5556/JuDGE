import json
import argparse
from crime_extraction import get_crime
from judge_extraction import calc_time_sum, calc_amt_sum
from law_extraction import get_penalcode_index_from_text

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
                gen_data[i] = item['gen_charge']
        return gen_data, exp_data
    

    def get_all_from_text(self, text):
        return get_crime(text), calc_time_sum(text), calc_amt_sum(text), get_penalcode_index_from_text(text)

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
            gen_crime = gen_ans

            crime_rec, crime_prec = self.calculate_recall_and_precision(exp_crime, gen_crime)

            # Accumulate the results
            self.total_crime_rec += crime_rec
            self.total_crime_prec += crime_prec


    def print_results(self):
        avg_crime_rec = self.total_crime_rec / self.n
        avg_crime_prec = self.total_crime_prec / self.n
       

        # Calculate F1 scores
        f1_crime = 2 * (avg_crime_prec * avg_crime_rec) / (avg_crime_prec + avg_crime_rec) if (avg_crime_prec + avg_crime_rec) != 0 else 0
        
        # Print the results

        print(f"Average Crime Recall: {avg_crime_rec:.4f}, Average Crime Precision: {avg_crime_prec:.4f}, F1 Score: {f1_crime:.4f}")



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
