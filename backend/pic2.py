from transformers import pipeline
from transformers import AutoImageProcessor, AutoModelForImageClassification
import json
import os

processor = AutoImageProcessor.from_pretrained("trpakov/vit-face-expression")
model = AutoModelForImageClassification.from_pretrained("trpakov/vit-face-expression")

pipe = pipeline("image-classification", model="trpakov/vit-face-expression")

def exec_pic(folder_path,output_path):
    sumres=[{"label": "angry", "score": 0.0}, 
            {"label": "fear", "score": 0.0},
            {"label": "happy", "score": 0.0}, 
            {"label": "neutral", "score": 0.0}, 
            {"label": "sad", "score": 0.0}]
    cnt=0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                result = pipe(file_path)  # 替换为图片路径
                result.sort(key=lambda result: result['label'])
                cnt+=1
                for i in range(len(result)): # 各个情绪分数求和
                    sumres[i]["score"]+=result[i]["score"]
                # print(f"picture {cnt}")
    if cnt==0:
        json_result=json.dumps(result)
        with open(output_path,'w') as fp:
            fp.write(json_result)
        return
    for item in sumres:
        item['score']/=cnt #取平均值
    json_result=json.dumps(result)
    with open(output_path,'w') as fp:
        fp.write(json_result)  # 输出分类结果
    return