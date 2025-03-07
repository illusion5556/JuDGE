import json
from data_segment_xingshi import DataSegmentXingshi
parser = DataSegmentXingshi(punctuation_replace=True)

with open('../../data/all.json') as file:
    data = json.load(file)

for item in data:
    wenshu = item["Full Document"]
    result = parser.parse(wenshu)
    for i in result:
        print(i, result[i])
        print('-'*50)
    
    print('*'*100)