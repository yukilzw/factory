'''
@Desc: openCV转换灰度图与轮廓判定
'''
import os
import json
import re
import cv2

dirPath = os.path.dirname(os.path.abspath(__file__))

milli_seconds = 50
milli_seconds_plus = milli_seconds
config = {}

# 输出灰度图与轮廓坐标集合
def output_clip(filename):
    global milli_seconds
    # 读取原图（这里我们原图就已经是灰度图了）
    img = cv2.imread(dirPath + '/clip/' + filename)
    # 转换成灰度图（openCV必须要转换一次才能喂给下一层）
    gray_in = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    # 反色变换，gray_in为一个numpy多维数组，代表着灰度图的色值0～255，我们将黑白对调
    gray = 255 - gray_in
    # 将灰度图转换为纯黑白图，要么是0要么是255，没有中间值
    _, binary = cv2.threshold(gray , 220 , 255 , cv2.THRESH_BINARY)
    # 保存黑白图做参考
    cv2.imwrite(dirPath + '/clip/invert-' + filename, binary)
    # 从黑白图中识趣包围图形，形成轮廓数据
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 解析轮廓数据存入缓存
    clip_list = []
    for item in contours:
        if item.size > 100:
            rows, _, __ = item.shape
            clip = []
            clip_list.append(clip)
            for i in range(rows):
                clip.append(item[i, 0].tolist())

    millisecondsStr = str(milli_seconds)
    config[millisecondsStr] = clip_list

    print(filename + ' time(' + millisecondsStr +') data.')
    milli_seconds += milli_seconds_plus

# 过滤算法返回的灰度图
clipFrame = []
for name in os.listdir(os.path.join(dirPath, 'clip')):
    if not re.match(r'^clip-frame', name):
        continue
    clipFrame.append(name)

clipFrameSort = sorted(clipFrame, key=lambda name: int(re.sub(r'\D', '', name)))
for name in clipFrameSort:
    output_clip(name)

jsObj = json.dumps(config)

fileObject = open(dirPath + '/mask.json', 'w')
fileObject.write(jsObj)
fileObject.close()

print('calc done')
