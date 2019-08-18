import time
import copy
import os
import hashlib
import cv2

class findFace(object):
    def __init__(self,imgName,originFileName):
        self.res_path = []
        self.path = None
        # 待检测的图片路径
        imagepath = './Test/static/wxtest/newface/'+originFileName
        # 获取训练好的人脸的参数数据
        face_cascade = cv2.CascadeClassifier('D:/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
        # 读取图片
        imageOrigin = cv2.imread(imagepath)
        os.remove(imagepath)
        sp = imageOrigin.shape
        img_h = sp[0]
        img_w = sp[1]
        #压缩图片尺寸
        if img_w >= 1280:
            img_1 = cv2.resize(imageOrigin, (1280,int(1280*img_h/img_w) ), interpolation=cv2.INTER_AREA)
            img_w = 1280
        elif img_w < 500:
            img_1 = cv2.resize(imageOrigin, (500,int(500*img_h/img_w) ), interpolation=cv2.INTER_AREA)
            img_w = 500
        else:
            img_1 = imageOrigin
        image = image = copy.deepcopy(img_1)
        # 探测图片中的人脸
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor = 1.15,
            minNeighbors = 5,
            minSize = ( int(img_w/10) , int(img_w/10) ),
            #flags = cv2.CASCADE_SCALE_IMAGE
        )
        if len(faces):
            md5 = hashlib.md5()   
            md5.update(str(image).encode("utf-8"))
            dirName = md5.hexdigest()
            if not os.path.exists('./Test/static/wxtest/newface/'+ dirName):
                os.mkdir('./Test/static/wxtest/newface/'+ dirName)
        for i,(x,y,w,h) in enumerate(faces):
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),5)
            #cv2.circle(image,((x+x+w)/2,(y+y+h)/2),w/2,(0,255,0),5)
            cutImg = img_1[y:y+h, x:x+w]
            localPath = 'static/wxtest/newface/'+ dirName +'/'+ str(i) + '^' +imgName
            cv2.imwrite('./Test/'+localPath, cutImg)
            self.res_path.append('python3.6.0/'+localPath)
        if len(faces):
            cv2.imwrite('./Test/static/wxtest/newface/'+ dirName +'/'+imgName, image)
            self.path = 'python3.6.0/static/wxtest/newface/'+ dirName +'/'+imgName
        cv2.waitKey(0)