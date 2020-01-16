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
from hashlib import sha1

import flutter_data, rn_game_center

# Generate session_id randomly
create_session_id = lambda: sha1(bytes('%s%s' % (os.urandom(16), time.time()), encoding='utf-8')).hexdigest()

class Session:
    # diy session

    info_container = {
        # session_id: {'user': info} --> Save user information, permissions, etc. via session
    }

    def __init__(self, handler):
        self.handler = handler

        # Get a random string as a session_id from the cookie, or generate a session_id if there is no or no match.
        random_str = self.handler.get_cookie('session_id')
        if (not random_str) or (random_str not in self.info_container):
            random_str = create_session_id()
            self.info_container[random_str] = {}
        self.random_str = random_str

        # Call set_cookie after each request.Ensure that the expiration time of each reset is XX seconds after the current time.
        self.handler.set_cookie('session_id', random_str, max_age=60)

    def __getitem__(self, item):
        return self.info_container[self.random_str].get(item)

    def __setitem__(self, key, value):
        self.info_container[self.random_str][key] = value

    def __delitem__(self, key):
        if self.info_container[self.random_str].get(key):
            del self.info_container[self.random_str][key]

    def delete(self):
        del self.info_container[self.random_str]

class SessionHandler:
    def initialize(self):
        self.session = Session(self)  # handler add session property

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
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(self.data)
    
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        if re.search(r"jsonp", self.request.path.lower()):
            self.write(self.get_argument('callback') + '(' + json.dumps(self.data) + ')')
        else:
            self.write(self.data)


class getRankList(SessionHandler, tornado.web.RequestHandler):
    def options(self):
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write({})

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
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
        (r"/socket/dy/flutter", flutter_data.dyFlutterSocket),
        (r"^/dy/flutter.+", flutter_data.dyFlutter),
        (r"^/dy/rn/gameCenter.+.+", rn_game_center.dyReactNativeGameCenter)
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

    tornado.ioloop.IOLoop.current().start()