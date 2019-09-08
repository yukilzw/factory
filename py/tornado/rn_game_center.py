import tornado, random, re

class dyReactNativeGameCenter(tornado.web.RequestHandler):
    def get(self):
        data = {
            "error": 0,
            "msg": "succ",
            "data": {
                "total": 223,
                "rows": []
            }
        }
        url = self.request.uri

        if re.search(r'/gameList|/search', url, re.I):
            page = self.get_argument("offset", default=1)
            listNum = 10
            if page == '2':
                listNum = 3
            i = 0
            while i < listNum:
                i += 1
                data["data"]["rows"].append(
                    {
                        "app_id": 418,
                        "icon": "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1567511527800&di=0cf9a9f2d23bb6c7f1ad928af8f0ce67&imgtype=0&src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fitem%2F201806%2F15%2F20180615222449_dcjkh.jpg",
                        "name": "精灵骑士团" + str(random.randint(0,10000)),
                        "cate": "dfgg",
                        "size": 100,
                        "memo": "这是一个有意思的游戏",
                        "link": "",
                        "has_gift": 1,
                        "has_task": 1,
                        "image": "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1568104496&di=4eca293c760ba1bc23bbd3bcc967ed84&imgtype=jpg&er=1&src=http%3A%2F%2Fpic1.win4000.com%2Fwallpaper%2F8%2F56ea3ff9aec6e.jpg",
                    }
                )

        self.write(data)

    def post(self):
        data = {
            "error": 0,
            "msg": "succ",
            "data": None
        }
        url = self.request.uri

        if re.search('/myGameIos', url, re.I):
            data["data"] = {
                "my_follow": [
                    {
                        "task_online_ts": 1587662298,
                        "gift_online_ts": 1567662298
                    }
                ]
            }

        self.write(data)