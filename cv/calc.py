import os, cv2, json

dirPath = os.path.dirname(os.path.abspath(__file__))

img = cv2.imread(dirPath + '/clip.png')

gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)

ret, binary = cv2.threshold(gray , 220 , 255 , cv2.THRESH_BINARY)

cv2.imwrite(dirPath + '/black.jpg', binary)

contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for item in contours:
    if item.size > 100:
        rows, _, __ = item.shape
        clip = []
        for i in range(rows):
            clip.append(item[i, 0].tolist())
            print(item[i][0])
            jsObj = json.dumps({
                'data': clip
            })
 
            fileObject = open(dirPath + '/mask' + str(item.size) + '.json', 'w')
            fileObject.write(jsObj)
            fileObject.close()
            

print('calc done')