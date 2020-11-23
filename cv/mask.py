import os, base64, requests, json, time

dirPath = os.path.dirname(os.path.abspath(__file__))
data = {
    'api_key': 'SgogTB9ZpBLwcEYAG4AXu4MkbNookgnJ',
    'api_secret': '2_lrgs8L1qjXf4by_Yi20CNcG3LtIYDc',
    'return_grayscale': 1
}

def reqfaceplus(reqTimes, filename):
    absName = os.path.join(dirPath, 'images', filename)
    files = {'image_file': open(absName, 'rb')}
    response = requests.post('https://api-cn.faceplusplus.com/humanbodypp/v2/segment', data=data, files=files)
    res = json.loads(response.text)
    reqTimes += 1
    print(filename +' req times:' + str(reqTimes))

    if 'error_message' in res:
        time.sleep(1)
        return reqfaceplus(reqTimes, filename)
    else:
        return res

for filename in os.listdir(os.path.join(dirPath, 'images')):
    res = reqfaceplus(0, filename=filename)

    img_data_color = base64.b64decode(res['body_image'])
    img_data = base64.b64decode(res['result'])
    # 注意：如果是"data:image/jpg:base64,"，那你保存的就要以png格式，如果是"data:image/png:base64,"那你保存的时候就以jpg格式。
    with open(dirPath + '/clip/clip-color-' + filename, 'wb') as f:
        f.write(img_data_color)
    with open(dirPath + '/clip/clip-' + filename, 'wb') as f:
        f.write(img_data)

print('mask created')
