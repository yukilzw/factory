# -*- coding: utf-8 -*-
# Mock data server,used for clients.

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.escape
import tornado.netutil
import tornado.process
import tornado.websocket
import asyncio, random, os, time, re, json, sys
from decorater.httpCrossHeader import header
from common.session import SessionHandler

import flutterData, rnGameCenter, uploadFile

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.write_message(json.dumps({
            "sign": "tornado", "data": "you has connected socket server~"
        }))
        pass

    def on_message(self, message):
        self.write_message(json.dumps({
            "sign": "tornado", "data": None
        }))

    def on_close(self):
        pass

class princeIndex(SessionHandler, tornado.web.RequestHandler):
    def get(self):
        debug = self.get_argument("debug", default='0')
        if debug == '1':
            self.render("prince-dev.html")
        else:
            self.render("prince.html")

class IndexHandler(SessionHandler, tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        print(self.get_secure_cookie('user_id'))
        self.set_secure_cookie('user_id', '123', expires=time.time()+900)
        user = self.session['user']
        if not user:
            yield self.render("index.html", username=None)
            return
        yield self.render("index.html",username=user)

class UserHandler(SessionHandler, tornado.web.RequestHandler):
    def post(self):
        user_name = self.get_argument("username")
        user_email = self.get_argument("email")
        user_website = self.get_argument("website")
        user_language = self.get_argument("language")
        self.session['user'] = user_name
        self.render("user.html",username=user_name,email=user_email,website=user_website,language=user_language)

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

def create_server():
    static_path = os.path.join(os.path.dirname(__file__), "static")
    template_path = os.path.join(os.path.dirname(__file__), "template")
    return tornado.web.Application([
        (r"/pysocket", WebSocketHandler),
        (r"/", IndexHandler),
        (r"/prince", princeIndex),
        (r"/user", UserHandler),
        (r"^/mock.+", princeMockMsg),
        (r"/test/getHourRank", getRankList),
        (r"/socket/dy/flutter", flutterData.dyFlutterSocket),
        (r"^/dy/flutter.+", flutterData.dyFlutter),
        (r"^/dy/rn/gameCenter.+.+", rnGameCenter.dyReactNativeGameCenter),
        (r"/upload", uploadFile.upload)
    ],
    template_path=template_path,
    static_path=static_path,
    cookie_secret="__TODO:LIU_ZHAN_WEI", debug=True)

if __name__ == "__main__":
    app = create_server()
    #app.listen(1236)

    sockets = tornado.netutil.bind_sockets(1236)
    #tornado.process.fork_processes(0)
    server = tornado.httpserver.HTTPServer(app)
    server.add_sockets(sockets)
    print('tornado start.')

    tornado.ioloop.IOLoop.current().start()