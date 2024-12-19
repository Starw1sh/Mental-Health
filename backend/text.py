import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import numpy as np  # 用于更好地格式化输出（可选）
import json
 
# 加载模型和标记器
# 来源：https://huggingface.co/michellejieli/emotion_text_classifier
model_name = "michellejieli/emotion_text_classifier"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
 
text = "This work is too hard for me. I want to give up."
 
# 对文本进行标记化和编码
inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
 
# 使用模型进行预测
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
 
# 获取softmax后的概率分布
probabilities = torch.nn.functional.softmax(logits, dim=1)
 
# 尝试从模型配置中获取标签列表（这取决于模型是否保存了这些信息）
try:
    labels = model.config.id2label
    # 获取预测的概率和对应的标签
    probs_and_labels = list(zip(probabilities[0].numpy(), labels.values()))  # 使用numpy来更好地处理数据
    list_data=[]
    for prob, label in probs_and_labels:
        if(label!='disgust' and label!='surprise'):
            if(label=='anger'):list_data.append({"label":'angry',"score":float(prob)})
            elif(label=='sadness'):list_data.append({"label":'sad',"score":float(prob)})
            elif(label=='joy'):list_data.append({"label":'happy',"score":float(prob)})
            else:list_data.append({"label":label,"score":float(prob)})
    # print(list_data)
    json_data=json.dumps(list_data)
    with open("../json/text.out","w") as fp:
        fp.write(json_data)
    # # 输出每个情绪的概率和标签
except AttributeError:
    # 如果模型配置中没有标签列表，你需要手动定义它们
    # 注意：这里的标签列表应该与模型训练时使用的标签列表相匹配
    print("Could not retrieve labels from model config. Please provide a labels list manually.")
 
# 如果你有标签列表但在这里没有使用它（比如从外部获取），你也可以这样使用它：
# labels = ["anger", "disgust", "fear", "happiness", "sadness", "surprise", "neutral"]
# 然后你需要确保logits的维度与标签列表的长度相匹配，并相应地调整上面的代码。