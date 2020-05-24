import tornado, json, random, re
from common.session import SessionHandler
from decorater.httpCrossHeader import header

class princeIndex(SessionHandler, tornado.web.RequestHandler):
    def get(self):
        debug = self.get_argument("debug", default='0')
        if debug == '1':
            self.render("prince-dev.html")
        else:
            self.render("prince.html")

class princeMockMsg(SessionHandler, tornado.web.RequestHandler):
    data = { "type": "From tornado server" }

    @header('Origin')
    def post(self):
        self.write(self.data)

    @header('Origin')
    def get(self):
        if re.search(r"jsonp", self.request.path.lower()):
            self.write(self.get_argument('callback') + '(' + json.dumps(self.data) + ')')
        else:
            self.write(self.data)


class getRankList(SessionHandler, tornado.web.RequestHandler):
    @header('Headers', 'Methods', 'Origin')
    def options(self):
        self.write({})

    @header('Origin')
    def get(self):
        page = self.get_argument("page", default=1)
        pageLimit = int(self.get_argument("pageLimit", default=5))
        data = {
            "error": 0,
            "msg": "ok",
            "data": []
        }
        i = 0
        while i < pageLimit:
            i += 1
            data["data"].append(
                {
                    "idx": (page - 1) * pageLimit + i,      # rank
                    "sc": random.randint(0,10000),          # score
                    "distance": i                           # distance
                }
            )
        self.write(data)