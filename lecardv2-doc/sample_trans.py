import json

id_ls=[]
with open('lecardv2_sample.json','r') as f:
    for item in f:
        item = json.loads(item)
        id_ls.append(item['text_id'])

res = []
with open('lecardv2-doc_all.json','r') as f:
    data = json.load(f)
    for item in data:
        if item['CaseId'] in id_ls:
            res.append(item)

with open('lecardv2-doc_sample.json','w') as f:
    json.dump(res,f,ensure_ascii=False,indent=4)