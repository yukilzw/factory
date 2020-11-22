import os, base64, requests, json

dirPath = os.path.dirname(os.path.abspath(__file__))
data = {
    'api_key': 'SgogTB9ZpBLwcEYAG4AXu4MkbNookgnJ',
    'api_secret': '2_lrgs8L1qjXf4by_Yi20CNcG3LtIYDc',
    'return_grayscale': 1
}
files = {'image_file': open(dirPath + '/images/504.jpg', 'rb')}
response = requests.post('https://api-cn.faceplusplus.com/humanbodypp/v2/segment', data=data, files=files)
res = json.loads(response.text)

# error_message

img_data_color = base64.b64decode(res['body_image'])
img_data = base64.b64decode(res['result'])
# 注意：如果是"data:image/jpg:base64,"，那你保存的就要以png格式，如果是"data:image/png:base64,"那你保存的时候就以jpg格式。
with open(dirPath + '/clip-color.png', 'wb') as f:
    f.write(img_data_color)
with open(dirPath + '/clip.png', 'wb') as f:
    f.write(img_data)

print('mask created')
