import json

with open('test.json','r',encoding='utf-8' )as f1,open("test_sft.json",'w',encoding='utf-8' )as f2:
  
    res = []
    lines = []
    for line in f1:
        lines.append(json.loads(line))
    for item in lines:       
        prompt = f"""
任务背景: 根据以下提供的案件事实，生成一份完整的刑法判决书。判决书需包括案件事实、法律分析、裁判理由以及最终裁判结论。
本案件事实：{item['text']}
本案件的完整判决书为：
"""
        item['prompt'] = prompt
        res.append(item)

    json.dump(res,f2,ensure_ascii=False,indent=4)