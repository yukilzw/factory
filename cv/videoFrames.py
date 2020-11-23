import os, cv2

dirPath = os.path.dirname(os.path.abspath(__file__))
cap = cv2.VideoCapture(dirPath + "/yoona.mp4")
c = 1
timeRate = .5  # 截取视频帧的时间间隔（这里是每隔10秒截取一帧）
 
while(True):
	ret, frame = cap.read()
	FPS = cap.get(5)
	if ret:
		frameRate = int(FPS) * timeRate  # 因为cap.get(5)获取的帧数不是整数，所以需要取整一下（向下取整用int，四舍五入用round，向上取整需要用math模块的ceil()方法）
		if(c % frameRate == 0):
			print("the number of frames：" + str(c))
			# 保存截取帧到本地
			cv2.imwrite(dirPath + "/images/frame" + str(c) + '.jpg', frame)
		c += 1
		cv2.waitKey(0)
	else:
		print("frames cut")
		break

cap.release()