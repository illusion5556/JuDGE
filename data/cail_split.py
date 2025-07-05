import json

test_id=[]
with open ('test.json', 'r') as f:
    for line in f:
        data = json.loads(line.strip())
        test_id.append(data['text_id'])

train_id=[]
with open ('train.json', 'r') as f:
    for line in f:
        data = json.loads(line.strip())
        train_id.append(data['text_id'])

with open('all_cail_ljp.json', 'r') as f1, open('cail_train.json', 'w') as f2, open('cail_test.json', 'w') as f3:
    for line in f1:
        data = json.loads(line.strip())
        if data['CaseId'] in train_id:
            f2.write(line)
        elif data['CaseId'] in test_id:
            f3.write(line)