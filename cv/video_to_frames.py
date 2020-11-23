'''
@Desc: 视频帧提取
'''
import os
import shutil
import cv2

dirPath = os.path.dirname(os.path.abspath(__file__))
images_path = dirPath + '/images'
cap = cv2.VideoCapture(dirPath + '/lisadance.mp4')
count = 1
time_rate = 50  # 截取视频帧的时间间隔

if os.path.exists(images_path):
    shutil.rmtree(images_path)
os.makedirs(images_path)

# 循环读取视频的每一帧
while True:
    ret, frame = cap.read()
    FPS = cap.get(5)

    if ret:
		# 因为cap.get(5)获取的帧数不是整数，需要取整
        frameRate = round(FPS, 0) * (time_rate / 1000)
        if(count % frameRate == 0):
            print('the number of frames：' + str(count))
            # 保存截取帧到本地
            cv2.imwrite(images_path + '/frame' + str(count) + '.jpg', frame)
        count += 1
        cv2.waitKey(0)
    else:
        print('frames were created successfully')
        break

cap.release()
