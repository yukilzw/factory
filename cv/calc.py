import os, cv2, json, re

dirPath = os.path.dirname(os.path.abspath(__file__))

milliseconds = 500
config = {}

def outputClip(filename):
    global milliseconds

    img = cv2.imread(dirPath + '/clip/' + filename)

    grayIn = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)

    gray = 255 - grayIn

    ret, binary = cv2.threshold(gray , 220 , 255 , cv2.THRESH_BINARY)

    cv2.imwrite(dirPath + '/clip/invert-' + filename, binary)

    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    clipList = []
    for item in contours:
        if item.size > 100:
            rows, _, __ = item.shape
            clip = []
            clipList.append(clip)
            for i in range(rows):
                clip.append(item[i, 0].tolist())

    millisecondsStr = str(milliseconds)
    config[millisecondsStr] = clipList

    print(filename + ' time(' + millisecondsStr +') data.')
    milliseconds += 500

clipFrame = []
for filename in os.listdir(os.path.join(dirPath, 'clip')):
    if not re.match(r'^clip-frame', filename):
        continue
    clipFrame.append(filename)

clipFrameSort = sorted(clipFrame, key=lambda name: int(re.sub(r'\D', '', name)))
for filename in clipFrameSort:
    outputClip(filename)

jsObj = json.dumps(config)

fileObject = open(dirPath + '/data/mask.json', 'w')
fileObject.write(jsObj)
fileObject.close()

print('calc done')