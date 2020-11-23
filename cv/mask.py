'''
@Desc: 调用算法模型接口返回人体灰度图
'''
import os
import shutil
import base64
import re
import json
import time
import requests

dirPath = os.path.dirname(os.path.abspath(__file__))
clip_path = dirPath + '/clip'

if os.path.exists(clip_path):
    shutil.rmtree(clip_path)
os.makedirs(clip_path)

data = {
    'api_key': 'SgogTB9ZpBLwcEYAG4AXu4MkbNookgnJ',
    'api_secret': '2_lrgs8L1qjXf4by_Yi20CNcG3LtIYDc',
    'return_grayscale': 1
}

def reqfaceplus(reqTimes, filename):
    abs_path_name = os.path.join(dirPath, 'images', filename)
    # 图片以二进制提交
    files = {'image_file': open(abs_path_name, 'rb')}
    response = requests.post('https://api-cn.faceplusplus.com/humanbodypp/v2/segment', data=data, files=files)
    res_data = json.loads(response.text)
    # 打印一下被限流的次数
    reqTimes += 1
    print(filename +' req times:' + str(reqTimes))
    # face++免费的API key很大概率被限流返回失败，所以我们递归调用（设个CD），一直等这个图片成功识别后再切到下一张图片
    if 'error_message' in res_data:
        time.sleep(.2)
        return reqfaceplus(reqTimes, filename)
    else:
        return res_data

# 读取之前准备好的所有视频帧图片进行识别
image_list = os.listdir(os.path.join(dirPath, 'images'))
image_list_sort = sorted(image_list, key=lambda name: int(re.sub(r'\D', '', name)))
for name in image_list_sort:
    res = reqfaceplus(0, filename=name)

    img_data_color = base64.b64decode(res['body_image'])
    img_data = base64.b64decode(res['result'])
    # 注意：如果是"data:image/jpg:base64,"，那你保存的就要以png格式
    # 如果是"data:image/png:base64,"那你保存的时候就以jpg格式。
    with open(dirPath + '/clip/clip-color-' + name, 'wb') as f:
        # 保存彩色图片
        f.write(img_data_color)
    with open(dirPath + '/clip/clip-' + name, 'wb') as f:
        # 保存灰度图片
        f.write(img_data)

print('mask created')
