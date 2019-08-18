import json,configparser,os,re
import urllib.request

def getConfig(section, key):
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/url.conf'
    config.read(path)
    return config.get(section, key)

PUBLIC = {
    "req_url" : getConfig("url","req_url")
}

buttonJson = {
    "button":[
        {    
            "type":"view",
            "name":"颜值打分",
            "url":"http://liuzhanwei.tunnel.echomod.cn/py/static/face/faceGradeGuide.html",
        },
        {
            "name":"医疗项目",
            "sub_button":[
                {    
                    "type":"view",
                    "name":"院内服务",
                    "url":"http://liuzhanwei2.tunnel.echomod.cn/yybdemo",
                },
                {    
                    "type":"view",
                    "name":"Vue预约挂号",
                    "url":"http://liuzhanwei2.tunnel.echomod.cn/vue-app",
                },
                {    
                    "type":"view",
                    "name":"ng5在线问诊",
                    "url":"http://liuzhanwei2.tunnel.echomod.cn/code/js-frame/askDoctor/dist",
                },
                {    
                    "type":"view",
                    "name":"聊天测试",
                    "url":"http://liuzhanwei.tunnel.echomod.cn/py/static/code/html/live/chat.html",
                },
            ]
        },
    ]
}

class wxSetButton(object):
    def __init__(self):
        self.getAssessToken()
    def getAssessToken(self):
        req = urllib.request.Request("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx73648417a7f020b2&secret=99c1a2788f166198b991c688bc19bd8c")
        res = urllib.request.urlopen(req)
        res_data =  json.loads(res.read())
        self.assess_token = res_data['access_token']
        self.setButton()
    def setButton(self):
        data = re.sub(r'\'', "\"",str(buttonJson)).encode("utf-8")
        req = urllib.request.Request("https://api.weixin.qq.com/cgi-bin/menu/create?access_token="+self.assess_token,data)
        res = urllib.request.urlopen(req)
        res_data = json.loads(res.read())
        print(res_data)

wxSetButton()