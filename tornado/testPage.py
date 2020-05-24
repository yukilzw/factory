import tornado, json, time
from common import session
from decorater.httpCrossHeader import header

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

class IndexHandler(session.SessionHandler, tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        # print(self.get_secure_cookie('user_id'))
        self.set_secure_cookie('user_id', '123', expires=time.time()+900)
        user = self.session['user']
        if not user:
            yield self.render("index.html", username=None)
            return
        yield self.render("index.html",username=user)

class UserHandler(session.SessionHandler, tornado.web.RequestHandler):
    def post(self):
        user_name = self.get_argument("username")
        user_email = self.get_argument("email")
        user_website = self.get_argument("website")
        user_language = self.get_argument("language")
        self.session['user'] = user_name
        self.render("user.html",username=user_name,email=user_email,website=user_website,language=user_language)