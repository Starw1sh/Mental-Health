from transformers import pipeline
from transformers import AutoImageProcessor, AutoModelForImageClassification
import json

processor = AutoImageProcessor.from_pretrained("trpakov/vit-face-expression")
model = AutoModelForImageClassification.from_pretrained("trpakov/vit-face-expression")

pipe = pipeline("image-classification", model="trpakov/vit-face-expression")
result = pipe(r"../upload/picture/test0.png")  # 替换为图片路径
result.sort(key=lambda result: result['label'])
json_result=json.dumps(result)
with open("../json/picture.out","w") as fp:
    fp.write(json_result)  # 输出分类结果
