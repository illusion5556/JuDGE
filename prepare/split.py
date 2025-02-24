import json
import random

def split_dataset(input_file, train_file, test_file, train_size, test_size, shuffle_seed=None):
    # Load the JSON data
    data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Set random seed if provided
    if shuffle_seed is not None:
        random.seed(shuffle_seed)
    
    # Shuffle the data initially
    if shuffle_seed is not None:
        random.seed(shuffle_seed)
    random.shuffle(data)
    
    # Ensure we have enough data to split
    if len(data) < train_size + test_size:
        raise ValueError("Not enough data to split the dataset as required.")
    
    # Split the data
    train_data = data[:train_size]
    test_data = data[train_size:train_size + test_size]
    
    # Function to transform data and add query_id
    def transform_data(data):
        transformed_data = []
        for item in data:
            entry = {
                "text_id": item['CaseId'],
                "text": item['Fact'],
                "la": item['Law Articles'],
                "fd": item['Full Document']
            }
            transformed_data.append(entry)
        return transformed_data
    
    # Transform the datasets
    train_data = transform_data(train_data)
    test_data = transform_data(test_data)
    
    # Save the training set
    with open(train_file, 'w', encoding='utf-8') as f:
        for item in train_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    # Save the testing set
    with open(test_file, 'w', encoding='utf-8') as f:
        for item in test_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"Dataset split completed.")
    print(f"Training set saved to {train_file} ({len(train_data)} records).")
    print(f"Testing set saved to {test_file} ({len(test_data)} records).")

# Example usage
if __name__ == "__main__":
    # Define file paths
    input_file = "../data/all.json"  # Replace with your input JSON file
    train_file = "../data/train.json"
    test_file = "../data/test.json"
    
    # Split the dataset with a shuffle seed for reproducibility
    split_dataset(input_file, train_file, test_file, train_size=2004, test_size=501, shuffle_seed=42)