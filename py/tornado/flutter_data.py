# dy_flutter DataCenter
import tornado, asyncio, random, requests, urllib, re, json, time
import time,threading

class dyFlutterSocket(tornado.websocket.WebSocketHandler):
    @staticmethod
    def sendMsg(self, message):
        asyncio.set_event_loop(asyncio.new_event_loop())
        try:
          i = 0
          while i < 20:
              index = random.randint(0, len(msgData) - 1)
              time.sleep(random.uniform(.1, .5))
              self.write_message(json.dumps(
                  (message, msgData[index])
              ))
              i += 1
        except tornado.websocket.WebSocketClosedError:
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
    'name': '迪丽热巴',
    'text': '我觉得这个主播长得还行叭~'
  }, {
    'lv': 80,
    'name': '古力娜扎',
    'text': '不如本小姐💗'
  }, {
    'lv': 3,
    'name': '吴彦祖',
    'text': '给我吴某人一个面子，你们两个不用争了，论颜值在座各位都是**，你们懂我的意思吧'
  }, {
    'lv': 50,
    'name': '吴亦凡',
    'text': '？？？'
  }, {
    'lv': 3,
    'name': '岳云鹏',
    'text': '你们这些人好像傻fufu的亚子...'
  }, {
    'lv': 50,
    'name': '郑爽',
    'text': '我来刷个屏幕~~~~666666666666666666666666666     ~~~~666666666666666666666666666'
  }, {
    'lv': -1,
    'name': '超管',
    'text': '楼上的黄牌警告一次！！！小心封号'
  }, {
    'lv': 50,
    'name': '郑爽',
    'text': '超管大哥我错了 o(TωT)o '
  }, {
    'lv': -1,
    'name': '超管',
    'text': '请各位按照直播间规定，文明发言，切勿刷屏，违者将封禁ID三天小黑屋反省，谢谢合作！'
  }, {
    'lv': 30,
    'name': '迪丽热巴',
    'text': '好的'
  }, {
    'lv': 80,
    'name': '古力娜扎',
    'text': '好哒'
  }, {
    'lv': 3,
    'name': '吴彦祖',
    'text': '我长的帅我说了算'
  }, {
    'lv': 50,
    'name': '吴亦凡',
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
      'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1572082173861&di=e5e040c062de8d2c56216205c4d95f9b&imgtype=0&src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fitem%2F201612%2F01%2F20161201234647_MPzZc.jpeg',
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
    'avatar': 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1577360261145&di=a8220b35b2635445f5bc6d7e89b7ff2f&imgtype=0&src=http%3A%2F%2Fimg08.oneniceapp.com%2Fupload%2Favatar%2F2018%2F08%2F02%2F68bb8d2db8a957c96da95fd20a46ee10.jpg',
    'sex': 1,
    'level': 80,
    'time': int(time.time()) - (24 * 60 * 60),
    'read': 159651,
    'title': '伞兵一号卢本伟准备就绪~',
    'content': '当年陈刀仔从20块赢到3700W，我卢本伟从20W赢到500W，冒得问题！',
    'pic': [
      'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1577360392463&di=127a2c1ea607d6591177e59f7df0ff5a&imgtype=0&src=http%3A%2F%2Fi2.hdslb.com%2Fbfs%2Farchive%2Fdae989eacbfad68b6d30c2e782cca329346e72ab.jpg',
      'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1577360406918&di=d21ed61d55e281dce4bcff653db5de00&imgtype=0&src=http%3A%2F%2Fn.sinaimg.cn%2Fsinacn12%2F294%2Fw640h454%2F20180911%2F137d-hiycyfw9543492.jpg',
      'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1577360406914&di=b63dd0f210d9d4a87e3368ef6b503ce3&imgtype=0&src=http%3A%2F%2F5b0988e595225.cdn.sohucs.com%2Fimages%2F20180218%2F1915abb20a294205b4c0bd2151176152.jpeg',
      'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1577360406910&di=a95c5103df899618d749dd1dc7e56dc4&imgtype=0&src=http%3A%2F%2Fi0.hdslb.com%2Fbfs%2Farchive%2Fdd921fe6d3c0cfd8ca56e4520340ab29dfdee0ac.jpg',
      'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1577360406909&di=2059b081847bbeb89ff3f572f5bec480&imgtype=0&src=http%3A%2F%2F5b0988e595225.cdn.sohucs.com%2Fimages%2F20171107%2F6060f478d6a6413596a5eef8ac196737.jpg'
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
    'name': '阿冷丶',
    'avatar': 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1577360894135&di=0b6ee5b73fff34d67c69a8978f5e9c93&imgtype=0&src=http%3A%2F%2F05imgmini.eastday.com%2Fmobile%2F20181228%2F20181228180936_b4beb4ab9c40eaf9f2b14b22c3af23ab_1.jpeg',
    'sex': 0,
    'level': 50,
    'time': int(time.time()) - (3 * 24 * 60 * 60),
    'read': 6541,
    'title': '今天嗓子有点痛，晚点播噢',
    'content': '大家可以去我的鱼吧为我的年度公会战打CALL，完成超级粉丝牌的任务，领取礼物道具（超级火箭、宇宙飞船）!',
    'pic': [
      'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1577360894134&di=de0116077c2fc9a96b79b128a8e600c2&imgtype=0&src=http%3A%2F%2Fwx3.sinaimg.cn%2Fcrop.0.0.1024.576%2F4ce4fe8ely1g04ku00i81j20sg0is0zx.jpg',
      'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1577360894132&di=0b1977e1ca9611300fc7ceb8f7b58548&imgtype=0&src=http%3A%2F%2Fi1.hdslb.com%2Fbfs%2Farchive%2F091147167360a5ec7a6525f273e7ee8a872e72de.jpg',
      'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1577360894131&di=d9ccf52a24a5f5abf1172cacefae8bc7&imgtype=0&src=http%3A%2F%2F5b0988e595225.cdn.sohucs.com%2Fimages%2F20180616%2F0b3f23499683436dafd2d8835672ee92.jpeg',
      'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1577360894095&di=1bc9cdd4a913a94ab1da50c11f66ab39&imgtype=0&src=http%3A%2F%2Fn.sinaimg.cn%2Fent%2Ftransform%2Fw630h945%2F20171218%2FuQL3-fypsqka8267152.jpg'
    ],
    'hot': 302,
    'discuss': [],
    'anchor': '冯提莫',
    'share': 65,
    'chat': 1201,
    'agree': 53,
    'isAgree': False
  }
]