import json 


with open('test_doc.json', 'r') as f1,open('test_doc_nothink.json', 'w') as f2:
    for item in f1:
        item = json.loads(item)
        item['input'] = item['input']+"/no_think"
        f2.write(json.dumps(item, ensure_ascii=False))
        f2.write('\n')
