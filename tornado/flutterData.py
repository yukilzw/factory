# dy_flutter DataCenter
import tornado, asyncio, random, requests, urllib, re, json, time
import time, threading

class dyFlutterSocket(tornado.websocket.WebSocketHandler):
    @staticmethod
    def sendMsg(self, message):
        asyncio.set_event_loop(asyncio.new_event_loop())
        i = 0
        while i < 20:
            try:
                index = random.randint(0, len(msgData) - 1)
                time.sleep(random.uniform(.1, .5))
                self.write_message(json.dumps(
                    (message, msgData[index])
                ))
                i += 1
            except Exception as e:
                pass

    @staticmethod
    def sendGift(self, message):
        asyncio.set_event_loop(asyncio.new_event_loop())
        try:
            for obj in giftData:
                time.sleep(1)
                self.write_message(json.dumps(
                    (message, obj)
                ))
        except tornado.websocket.WebSocketClosedError:
          pass

    def on_message(self, message):
        if message == 'getChat':
            fuc = dyFlutterSocket.sendMsg
        elif message == 'getGift':
            fuc = dyFlutterSocket.sendGift
        t = threading.Thread(target=fuc, args=(self, message))
        t.start()

    def on_close(self):
        pass
    
    def open(self):
        pass

class dyFlutter(tornado.web.RequestHandler):
    def getliveData(self):
        param = {
            'type': 'yz',
            'page': self.get_argument("page", default='1')
        }
        values = urllib.parse.urlencode(param)
        response = requests.request('GET', 'https://m.douyu.com/api/room/list?' + str(values), stream=True)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return liveData

    def lotteryResult(self):
        index = random.randint(0,7)
        return gift[index]

    def addId(self, yubaList):
        result = []
        for item in yubaList:
            item['id'] = str(random.random())
            result.append(item)
        return result

    async def post(self):
        data = await self.handel()

        self.write(data)

    async def get(self):
        data = await self.handel()

        self.write(data)

    async def handel(self):
        data = {
            "error": 0,
            "msg": "ok"
        }
        url = self.request.uri

        if re.search('/nav', url, re.I):
            data["data"] = nav
        elif re.search('/swiper', url, re.I):
            data["data"] = swiperPic
        elif re.search('/broadcast', url, re.I):
            data["data"] = broadcastSwiper
        elif re.search('/liveData', url, re.I):
            data = self.getliveData()
        elif re.search('/giftData', url, re.I):
            data["data"] = giftData
        elif re.search('/msgData', url, re.I):
            data["data"] = msgData
        elif re.search('/yubaList', url, re.I):
            data["data"] = self.addId(yubaList)
        elif re.search('/lotteryConfig', url, re.I):
            data["data"] = lotteryConfig
        elif re.search('/lotteryResult', url, re.I):
            await asyncio.sleep(.9)
            data["data"] = self.lotteryResult()

        return data

# default Data
gift = [
  {
    'giftName': '100鱼丸',
    'giftIndex': 0
  },
  {
    'giftName': '礼物道具棒棒哒 × 1',
    'giftIndex': 1
  },
  {
    'giftName': '鲲抱枕 × 1',
    'giftIndex': 2
  },
  {
    'giftName': '谢谢参与',
    'giftIndex': 3
  },
  {
    'giftName': '礼物道具弱鸡 × 1',
    'giftIndex': 4
  },
  {
    'giftName': '蔡文姬手办 × 1',
    'giftIndex': 5
  },
  {
    'giftName': '100Q币',
    'giftIndex': 6
  },
  {
    'giftName': '10Q币',
    'giftIndex': 7
  }
]

nav = [
    '推荐', '英雄联盟', '绝地求生', '王者荣耀', '和平精英', '颜值',
    '一起看', '户外', 'DNF', '穿越火线', '主机游戏', '二次元', 'DOTA2'
]

swiperPic = [
  'http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/wzxpaHPxJTBumQ3R6Ez3ufbizm..nLWocdZhFoXbVnU!/r/dL8AAAAAAAAA',
  'http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/9zkbiqeCxnkGCgpweQoEUWlNeaNL.Y96vuQAdo70sD0!/r/dL8AAAAAAAAA',
  'http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/QZ1KSYcJo5Sw.ozGrAHLaHFstl*0LCo9GAk.JedFoOs!/r/dFIBAAAAAAAA',
  'http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/RlEg9VTbPdmilUBXHwqEFXMSIyKlOpolovzFRq0.*DE!/r/dLgAAAAAAAAA',
  'http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/hVYSRAuV2YZgZ0bDAVPhekvuckqmTZQsCgL.vIyVXbw!/r/dFQBAAAAAAAA',
  'http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/kXX56r1pIU.XFf.wr4mF3pwRBV9vX9qvGJg4sx1uE0k!/r/dE8BAAAAAAAA'
]

broadcastSwiper = [
  {
    'title': '斗鱼主播换机季',
    'time': 1578480528,
    'num': 22165,
    'order': False
  },
  {
    'title': '回归游戏，导师学员各显申通，最劲爆的PK场景',
    'time': 1581504528,
    'num': 22165,
    'order': True
  }
]

liveData = {
    "code": 0,
    "data": {
        "list": [
            {
                "rid": 6597095,
                "vipId": 0,
                "roomName": "【唱跳主播】试图温柔的舞蹈主播",
                "cate1Id": 0,
                "cate2Id": 311,
                "roomSrc": "http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/sSITT7Yd3McRebgfEhWZVy3GOWiwtRsb86CuLWP18qg!/r/dMMAAAAAAAAA",
                "avatar": "http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/Uek2RBFDyQKZw4eWhn0yCDJl.pSFEoVjSRNyjrpTHVM!/r/dL4AAAAAAAAA",
                "nickname": "阿让让丶",
                "isVertical": 0,
                "liveCity": "鱼塘",
                "isLive": 1,
                "hn": "1192.1万"
            }, {
                "rid": 968987,
                "vipId": 0,
                "roomName": "腿长2m会跳舞的模特妹妹呀",
                "cate1Id": 0,
                "cate2Id": 311,
                "roomSrc": "http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/YlBFCPPvdoeqNuGfTS2fJz3pRIjiFb3xlLogWon5pc0!/r/dL8AAAAAAAAA",
                "avatar": "http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/YyHKHSXyJ8zZD76nfSrYPECV65NrmrW6NrO46RwO52Y!/r/dLYAAAAAAAAA",
                "nickname": "南妹儿呀",
                "isVertical": 0,
                "liveCity": "鱼塘",
                "isLive": 1,
                "hn": "25.5万"
            }, {
                "rid": 513890,
                "vipId": 0,
                "roomName": "山东小甜甜",
                "cate1Id": 0,
                "cate2Id": 201,
                "roomSrc": "http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/l.AHxX3DD7copb4a3B7E.EA0VE0HyRCJx5*p7uWyFOI!/r/dFMBAAAAAAAA",
                "avatar": "http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/FBhyivqv7BViM2VHWZKmoczfCQUp.NJz9ERaceJVJZQ!/r/dFIBAAAAAAAA",
                "nickname": "大美人虞姬",
                "isVertical": 1,
                "liveCity": "鱼塘",
                "isLive": 1,
                "hn": "38.8万"
            }, {
                "rid": 6611509,
                "vipId": 0,
                "roomName": "想不出标题 想你",
                "cate1Id": 0,
                "cate2Id": 201,
                "roomSrc": "http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/h6mA07Rv.RduJhomiKoqzZw5Pz2aCUJa5hUwRqEyGjU!/r/dMMAAAAAAAAA",
                "avatar": "http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/lnNVlzMIH7ptD1dH7Xd6JcalaWd.Sg3zIwM7CF5.i00!/r/dFQBAAAAAAAA",
                "nickname": "你的怡宝阿",
                "isVertical": 1,
                "liveCity": "孝感市",
                "isLive": 1,
                "hn": "4.8万"
            }, {
                "rid": 910907,
                "vipId": 0,
                "roomName": "凉凉小主播回来了",
                "cate1Id": 0,
                "cate2Id": 201,
                "roomSrc": "http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/vbuK5Lc9B86b7RfvROZzlbP.8hGdJPojTTsabOWSDYM!/r/dLgAAAAAAAAA",
                "avatar": "http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/9iN5AqTsytMeLcWQ56xLgtYX*CfeHYPJ1eqqj4p5OTM!/r/dL8AAAAAAAAA",
                "nickname": "流口水的小熊猫",
                "isVertical": 1,
                "liveCity": "大连市",
                "isLive": 1,
                "hn": "138.4万"
            }, {
                "rid": 5324159,
                "vipId": 0,
                "roomName": "15号晚上八点周年庆啦，欢迎大家",
                "cate1Id": 0,
                "cate2Id": 201,
                "roomSrc": "http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/SnDeyEXwOYE9kd6Qt6tOiR6Jd15ZPv1hHNs745fHU.g!/r/dL8AAAAAAAAA",
                "avatar": "http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/FhbZBofWLBP22xjfHDoYUjsJSqD4oyl2quqvbMDzv74!/r/dAcBAAAAAAAA",
                "nickname": "白菜mm丶",
                "isVertical": 1,
                "liveCity": "无锡市",
                "isLive": 1,
                "hn": "429.2万"
            }, {
                "rid": 5656277,
                "vipId": 0,
                "roomName": "对不起我又没洗头",
                "cate1Id": 0,
                "cate2Id": 201,
                "roomSrc": "http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/so*Ld8iEATZeylfdoFtPzlQoC5AOrW8rk9YplPNMNN0!/r/dIMAAAAAAAAA",
                "avatar": "http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/AwZhsgPh44XckW2bylNQP2io3JxB714xeW4.mHZL4eY!/r/dL8AAAAAAAAA",
                "nickname": "美羊羊公举",
                "isVertical": 1,
                "liveCity": "苏州市",
                "isLive": 1,
                "hn": "57.8万"
            }, {
                "rid": 1997783,
                "vipId": 0,
                "roomName": "治愈系甜美邻家女孩~",
                "cate1Id": 0,
                "cate2Id": 311,
                "roomSrc": "http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/ZOakGzN3uA8nHAsl8coF.15GVERdNHp.ZjfnywFIP8w!/r/dL8AAAAAAAAA",
                "avatar": "http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/uoNTLkHhh1O2M90WWKCpe*Qf5K0tWVpbePLcgI8VOvk!/r/dMMAAAAAAAAA",
                "nickname": "迎接太阳的庆",
                "isVertical": 0,
                "liveCity": "鱼塘",
                "isLive": 1,
                "hn": "64.7万"
            }, {
                "rid": 4566947,
                "vipId": 0,
                "roomName": "你的小可爱已到货快来签收",
                "cate1Id": 0,
                "cate2Id": 201,
                "roomSrc": "http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/7RnWwkhUOkzWkHNSjdljh*6*tkcHTz5CngbWQ2ct4nY!/r/dDQBAAAAAAAA",
                "avatar": "http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/pyIDMIBofTjdLKhBKnFgv*9CSpktrXnm0AxUeGywAoI!/r/dMUAAAAAAAAA",
                "nickname": "关晓羽",
                "isVertical": 1,
                "liveCity": "鱼塘",
                "isLive": 1,
                "hn": "22.3万"
            },
        ]
    }
}

giftData = [
    {
    'giftName': ' 超级火箭',
    'giftImg': 'http://m.qpic.cn/psb?/V14dALyK4PrHuj/JvlEbGsGmSTzXOCcXJjztMLP71lc2SS5e6wdxTQSBaw!/b/dL4AAAAAAAAA',
    'avatar': 'http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/wTg*ymRR70vh10HRN.iRvN0PWCy.kPJIOIxsBMjkiAk!/r/dFQBAAAAAAAA',
    'nickName': '智勋勋勋勋勋勋勋'
    }, {
    'giftName': '飞机',
    'giftImg': 'http://m.qpic.cn/psb?/V14dALyK4PrHuj/8WI1OXFOx1HnUQccFLNhp5lrP9pt.TMI0McJ9HJniKM!/b/dL8AAAAAAAAA',
    'avatar': 'http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/twWFVdhN5s70wTUvl*hCCLeI.qXkxWSMhMwRa9yUqMY!/r/dL4AAAAAAAAA',
    'nickName': 'XDD'
    }, {
    'giftName': '情书',
    'giftImg': 'http://m.qpic.cn/psb?/V14dALyK4PrHuj/FcXcq*5KJrUoF.JnNkg1d8FLfGO89RLlhVn0fRK5xqM!/b/dLYAAAAAAAAA',
    'avatar': 'http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/sgZQ0hOAExezr*RXn*M.2MsKGHx3u6qrYGyrxTeAPcs!/r/dLsAAAAAAAAA',
    'nickName': '妃凌雪'
    }, {
    'giftName': '冷醤BoBo',
    'giftImg': 'http://m.qpic.cn/psb?/V14dALyK4PrHuj/Z8I8wBsay0e2xLCbrgy6PZNRj1BASXVHWfqeIOtvMEQ!/b/dDABAAAAAAAA',
    'avatar': 'http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/ch4tK*lEnQ3CzEK726Mw6AJFG*DX*t3aYQZOUI0c0VA!/r/dMMAAAAAAAAA',
    'nickName': '阿冷丶'
    }
]

msgData = [
  {
    'lv': 30,
    'name': '土块',
    'text': '我觉得这个主播长得还行叭~'
  }, {
    'lv': 80,
    'name': '周淑怡',
    'text': '不如本小姐💗'
  }, {
    'lv': 3,
    'name': '智勋勋勋勋',
    'text': '给我勋某人一个面子，你们两个不用争了，论颜值在座各位都是**，你们懂我的意思吧'
  }, {
    'lv': 50,
    'name': '芜湖大司马',
    'text': '？？？'
  }, {
    'lv': 3,
    'name': '余小C',
    'text': '你们这些人好像傻fufu的亚子...'
  }, {
    'lv': 50,
    'name': '腐团儿',
    'text': '别冲了兄弟们~~~~这个腿也没我长啊，有什么好看的呢'
  }, {
    'lv': -1,
    'name': '超管',
    'text': '楼上的黄牌警告一次，满两次将会被禁言！'
  }, {
    'lv': 50,
    'name': 'SKT.Faker',
    'text': '내가 틀렸다...'
  }, {
    'lv': -1,
    'name': '超管',
    'text': '请各位按照直播间规定，文明发言，切勿刷屏，违者将封禁ID三天小黑屋反省，谢谢合作！'
  }, {
    'lv': 30,
    'name': '土块',
    'text': '好的'
  }, {
    'lv': 80,
    'name': '周淑怡',
    'text': '好哒'
  }, {
    'lv': 3,
    'name': '余小C',
    'text': '我长的帅我说了算'
  }, {
    'lv': 50,
    'name': '阿冷丶',
    'text': '哦'
  },
]

lotteryConfig = {
  'pageBg': 'http://m.qpic.cn/psb?/V14dALyK4PrHuj/34o8GU5chGip*chFO*A0jNcqn3Gc0Alomq1ZvxGhsZs!/b/dL8AAAAAAAAA',
  'pageH': 546.0,
  'lotteryBg': 'http://m.qpic.cn/psb?/V14dALyK4PrHuj/2uQoAkAV1UGZ2Y3seRWPU6vLyS*OC*4WM1hS**Uva48!/b/dL8AAAAAAAAA',
  'lotteryH': 236.0,
  'lotteryW': 351.0,
  'highLightBg': 'http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/7negjfbFqhI7YGRpJvJ7HhQVw6mrUIF3iRaImzbca2g!/r/dLYAAAAAAAAA',
  'myRewardBg': 'http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/jUoeVWEPqaH7eFbZF0e*KtDMZBu8sRcHjCdVq8yhkg4!/r/dL4AAAAAAAAA',
  'myRewardH': 25.0,
  'myRewardW': 86.0
}

yubaList = [
  {
    'id': '', # 动态注入
    'name': '小玉太难了丶',
    'avatar': 'http://r.photo.store.qq.com/psb?/V14dALyK4PrHuj/9iN5AqTsytMeLcWQ56xLgtYX*CfeHYPJ1eqqj4p5OTM!/r/dL8AAAAAAAAA',
    'sex': 0,
    'level': 30,
    'time': int(time.time()) - (1 * 60 * 60),
    'read': 159651,
    'title': '10月24日晚六点，我再斗鱼3168536等你！！！不见不散哦！',
    'content': '观众姥爷们，我正方形主播玉酱回来啦！24号晚六点，斗鱼房间3168536，我再直播间等你们！还有精彩好礼，不停放送！！',
    'pic': [
      'http://r.photo.store.qq.com/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEFXFXnQhjxD.WofABoFG.o3*Qsf0oyF5yrWlQ3Y4FnSwIWL8CnUcQD2gU6GX5YvK*r3jZzspTjUxfbN7XIQ9crk!/r',
    ],
    'hot': 82,
    'discuss': [
      {
        'from': '醉音符',
        'talk': '小姐姐终于开播了，火车开起来！'
      },
      {
        'from': '小流仔丶QAQ',
        'to': '醉音符',
        'talk': '你怎么像个魔教中人？'
      }
    ],
    'anchor': '一条小团团',
    'share': 129,
    'chat': 2156,
    'agree': 13542,
    'isAgree': True
  },
  {
    'id': '',
    'name': 'white五五开',
    'avatar': 'http://r.photo.store.qq.com/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEOJgoW6KQuTNSROq4QzcEpt3ypSQF3ctaoyaNJhNMsUd5kTivEoEHlccAKKD85M9rPs4dvOrSPp.FPq7c98m*dM!/r',
    'sex': 1,
    'level': 80,
    'time': int(time.time()) - (24 * 60 * 60),
    'read': 159651,
    'title': '伞兵一号卢本伟准备就绪~',
    'content': '当年陈刀仔从20块赢到3700W，我卢本伟从20W赢到500W，冒得问题！',
    'pic': [
      'http://r.photo.store.qq.com/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrECsCoxbUqGDiWCzcCaMNadpwNNOrQN6fdFFKDO7vMXnvSGeJy4fIuwTkad1EVo*8KTs.wWyjV01LE55uOcDwRTY!/r',
      'http://r.photo.store.qq.com/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEJ*ktPg3BnrtOB5ZlyJzD2SDnD8wR9HRaUvfDA8VX3A26WibY3SksDe0oPQftdtt0wysn*DK5fZfxFRHUlZWWkI!/r',
      'http://r.photo.store.qq.com/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEH.Zo3e9KhfjDzTIDfSQJJiey2YYEgWGG4Dv6w73RfqI.4m1BHVfElCuoxxS9X63QAl2qF9XlV0sLZEEpIbvtoc!/r',
      'http://r.photo.store.qq.com/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEAJncDUDBvW3iBYqeMnPJF*XkLGmOB8vpYIe2Xzswwo0WGVygTowfdpkaML9qNvY1oPE2*agf4LQomuYDITfb5A!/r',
      'http://r.photo.store.qq.com/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEJ1k8vVccix*AD5fgYJH*Krioh2CYy8aA0Wwqf0vgkBsLDzwJO5l28Hggx1aKzBb72VH2tswn7d*aqRt2aIyUEk!/r'
    ],
    'hot': 82,
    'discuss': [
      {
        'from': '马飞飞',
        'talk': '哇，牛逼啊开哥'
      },
      {
        'from': '五五开',
        'talk': '难受啊马飞'
      }
    ],
    'anchor': '芜湖大司马',
    'share': 12546,
    'chat': 5236541,
    'agree': 210259,
    'isAgree': False
  },
  {
    'id': '',
    'name': '智勋勋勋勋',
    'avatar': 'http://r.photo.store.qq.com/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEOm3cTsYX71M9wKWjRwCJhrQiBGA0m.YNqml6jjWgwgLGABbVNiERNjTQnyESyDkhACpMUjBoToHs*aaLIz9OW4!/r',
    'sex': 1,
    'level': 50,
    'time': int(time.time()) - (4 * 60 * 60),
    'read': 12564,
    'title': '小姐姐你有凉快点的照片吗',
    'content': '大家赶紧去给这个比心小姐姐点个赞，我靠这谁顶得住啊？',
    'pic': [
      'http://r.photo.store.qq.com/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrECn*5X45UmCjjXB.BfckpGWRRM4PF1NLvcSQ4SXfavucz5VN02pTwU51PSUxMXCwIRR2ECmU*ETLaHJbVE7o0LE!/r',
      'http://r.photo.store.qq.com/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEB*OV*zvzMDwQAplUUcur1rIYIAWBVPfYoY.oI1Cu1NR7cykHqHtf9WSb0PBmP7kR1w8EF4pPzbanlLr4RpOR*g!/r',
      'http://r.photo.store.qq.com/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEJEqqDxPOtzgToC5ZXShd4oH1kK3j9hVYcyNKfcYjdXSsXUrEjbxlsJXNQDwzWDehmmBHdx4YTkos83Sb04fN5o!/r',
      'http://r.photo.store.qq.com/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEGj5RcO1yCznjMgFp83vSiQAdZJu0voQstcek8r5s48OppINPkqKwhnrhgYyRXAwodhdWCf08wkpfmcT5BCMYQI!/r'
    ],
    'discuss': [
      {
        'from': 'Linke',
        'talk': '约德尔老乡'
      },
      {
        'from': '呆妹儿小霸王',
        'talk': '这声老公我先叫了'
      }
    ],
    'hot': 2104,
    'anchor': '教主',
    'share': 65,
    'chat': 41,
    'agree': 120,
    'isAgree': False
  },
  {
    'id': '',
    'name': 'LISA',
    'avatar': 'http://m.qpic.cn/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrECvfZzzliPnLwXD4Alsi2yA3GUm5wWAXmgTj43bJgEzupvL8T7RmPkWT*jzxj7MXsQgPzwnvz8PO06WYKN2UyTE!/b&bo=6APoAwAAAAABFzA!&rf=viewer_4',
    'sex': 0,
    'level': 80,
    'time': int(time.time()) - int(0.8 * 24 * 60 * 60),
    'read': 6541,
    'title': '大家好，我是LISA',
    'content': '请大家多多关注black pink~',
    'pic': [
      'http://m.qpic.cn/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEHCSn278EIS.Ztco0pQyXjluqAqZMrICcvAmOP4mj8EqkekgUbR37DW7NLd3hTGYVwmjUDffgxP.OYWdsCqltk4!/b&bo=gAI1BAAAAAABF4M!&rf=viewer_4',
      'http://m.qpic.cn/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEGdFIO4rj7fZrgFFYv.Drd.fZx.Oe6eMFdOuBqpJhHwkHQ4NuVZk3UmVv4.OMy5PWgFBWNeVycjanXtPWNAxwUE!/b&bo=6ANYAwAAAAABF4A!&rf=viewer_4',
      'http://m.qpic.cn/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEKuZ9ll.0XkofwHW*m64Bp1dOMRCQ2pnpn6RMkjuSshs6IeI*agGmrbNK0RjyHkV*QP1OoYo**JiW1z8uIDpIww!/b&bo=vAK7AgAAAAABFzc!&rf=viewer_4',
      'http://m.qpic.cn/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEO9csxxCYlKtBIG6.wMMwluHhD8DNk1NsCD3aJyLtkeXT*R*qB4HTk63C17hW4uU6ERhJLBfGhX9vY6*DVWOlyo!/b&bo=vAK8AgAAAAABFzA!&rf=viewer_4',
      'http://m.qpic.cn/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEFhXimhpeW9.dDCWHqvwg9M4Ihj4OrIptUtyclYhzU75OK2vXBJWH61ZvLcW9Wjpvnoo.*mCx*4Hkg7gLlWiLyk!/b&bo=gAIABAAAAAABF7Y!&rf=viewer_4',
      'http://m.qpic.cn/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEGN5jKxQsdTPWbK8dPkikNehC86NVtjF46CdBDIOPwDifSigMVU1FkVVNedUeMcZ1w3IqSMgn5QRCPRNAZh2pag!/b&bo=9AHvAQAAAAABFys!&rf=viewer_4',
      'http://m.qpic.cn/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEHxlnNj9aAtqPCwrIXIWIqTjOc8loKpGtYRmPgrkf*d3VAVtQhA5C2pDID3djK9GtzBK8Seoo*zWCS3plHfOVPw!/b&bo=kAGQAQAAAAABFzA!&rf=viewer_4',
      'http://m.qpic.cn/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEIr7POmXYwwkOHrKpfx*6fpeAwD9uhw88hOeRBsZQkllPF0jho2nxi5RERFbZTXa1eEFojBv*ZPl9aBFoerWb10!/b&bo=9AFvAgAAAAABF6g!&rf=viewer_4',
      'http://m.qpic.cn/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEPgIXM4foZiWA0JJ..bpBSmAiBwX7ZiFrFIlNsv*L8a0kKzzDZqmG3BdOQd*6gAKLAPkwvAO87hblyCU8Rme9aQ!/b&bo=kAELAQAAAAABF6s!&rf=viewer_4'
    ],
    'hot': 65488,
    'discuss': [],
    'anchor': 'BLACK PINK',
    'share': 1412,
    'chat': 32105,
    'agree': 12541,
    'isAgree': False
  },
  {
    'id': '',
    'name': '阿冷丶',
    'avatar': 'http://r.photo.store.qq.com/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEHBmteT44aHk5h9nmbSDWpjWQ.N.OpM5cG6kvhzRmYFUOGmzfpfaV6zqxvelW*3fxmpTZfckafPLvHCVGI0Gi28!/r',
    'sex': 0,
    'level': 50,
    'time': int(time.time()) - (3 * 24 * 60 * 60),
    'read': 6541,
    'title': '今天嗓子有点痛，晚点播噢',
    'content': '大家可以去我的鱼吧为我的年度公会战打CALL，完成超级粉丝牌的任务，领取礼物道具（超级火箭、宇宙飞船）!',
    'pic': [
      'http://r.photo.store.qq.com/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEKIimZ5ku35IiB8ouply3mTf3g7iWuQYCqUpNL7.mSvc6mzJit49pKLE2RXrl0x.C9Rx1y6emL7ubCY1RM.dMWI!/r',
      'http://r.photo.store.qq.com/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrEDCYhcAUpTOjnoUbyD4lEX4Ul9Bl1m.ftzH5.zz3scTc2r93dT*107hNKmyla5A.dWvtlOBdU2EUTzL8Nllgdeo!/r',
      'http://r.photo.store.qq.com/psc?/V14dALyK4PrHuj/TmEUgtj9EK6.7V8ajmQrELzHcDo*Xy6D31j9lVnpncYpkGWS0Cql7Xf3yNfo5mFPTOAesA*stTQBNUVv6Ja2E.4*3Fl8jru*7*J*i7Z.FyY!/r'
    ],
    'hot': 302,
    'discuss': [],
    'anchor': '呆妹儿',
    'share': 65,
    'chat': 1201,
    'agree': 53,
    'isAgree': False
  }
]