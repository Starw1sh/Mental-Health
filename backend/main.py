def print_log(str):
    with open("Log.txt","a",encoding='UTF-8') as fp:
        fp.write(str)
        fp.write("\n")
    print(str)

def log(str):
    with open("Log.txt","a",encoding='UTF-8') as fp:
        fp.write(str)
        fp.write("\n")

with open("Log.txt","w",encoding='UTF-8') as fp: # clear the Log
    pass
import pic2
log("pic2 init")
import text
log("text finish")
import video
video.main()
log("video finish")

pic2.exec_pic("../upload/picture/","../json/picture.out")
pic2.exec_pic("./output_faces","../json/video.out")

import requests
import json

def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
        
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=igNRCRER1H6GKVBPlQ6vsX4s&client_secret=DjiGZ99nOGi3uuTlg1r6cWUbzPn4rhi7"
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def main():
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()
    
    with open("../json/text.out",'r') as fp:
        textout=fp.read()
    with open("../json/video.out",'r') as fp:
        videoout=fp.read()
    with open("../json/picture.out",'r') as fp:
        picout=fp.read()
    log("ask")
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "你是一个心理学专家，下面是根据一个同学近期的视频、图像和网上发言文本分析出来的情绪指标。近期学校进行了一次期中测试，而该同学在期中测试中的成绩并不理想。\
                            请根据这些情绪指标分析他目前的心理状态。如果有问题，给出可能的解决方案。\n"+"视频指标："+videoout+"\n"+"图像指标：\
                            "+picout+"\n"+"文本指标"+textout+"\n"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    result_dict = json.loads(response.text)
    print_log(result_dict["result"])
    

if __name__ == '__main__':
    main()