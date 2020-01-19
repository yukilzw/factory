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
                        "icon": "",
                        "name": "精灵骑士团" + str(random.randint(0,10000)),
                        "cate": "dfgg",
                        "size": 100,
                        "memo": "这是一个有意思的游戏",
                        "link": "",
                        "has_gift": 1,
                        "has_task": 1,
                        "image": None,
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