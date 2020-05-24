import urllib,json,threading

#获取access_token,jsapi_ticket类
class getAssessToken(object):
    def __init__(self):
        try:
            self.assess_token
            timer = threading.Timer(1.99*60*60, self.getToken)
            timer.start()
        except AttributeError:
            self.getToken()
    def getToken(self):
        req = urllib.request.Request("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx73648417a7f020b2&secret=99c1a2788f166198b991c688bc19bd8c")
        res = urllib.request.urlopen(req)
        res_data =  json.loads(res.read())
        self.assess_token = res_data['access_token']
        print("获取的token为 ： "+self.assess_token)
        self.getTicket()
        self.__init__()
    def getTicket(self):
        req = urllib.request.Request('https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token='+self.assess_token+'&type=jsapi')
        res = urllib.request.urlopen(req)
        res_data =  json.loads(res.read())
        self.ticket = res_data['ticket']
        print("获取的ticket为 ： "+self.ticket)