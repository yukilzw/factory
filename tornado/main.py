# -*- coding: utf-8 -*-
# Mock data server,used for clients.
import os
from decorater.httpCrossHeader import header
from common.session import SessionHandler
import tornado.web
import tornado.websocket
import flutterData, rnGameCenter, uploadFile, princeSpa, testPage

class taskConfig(SessionHandler, tornado.web.RequestHandler):
    @header('Headers', 'Methods', 'Origin')
    def options(self):
        self.write({})

    @header('Origin')
    def get(self):
        with open(os.path.join(os.path.dirname(__file__), 'static/taskConfig.js'), 'r') as f:
            self.write(f.read())

class Index(SessionHandler, tornado.web.RequestHandler):
    @header('Headers', 'Methods', 'Origin')
    def options(self):
        self.write({})

    @header('Origin')
    def get(self):
        with open(os.path.join(os.path.dirname(__file__), 'static/dist/index.html'), 'r') as f:
            self.write(f.read())

def create_server():
    static_path = os.path.join(os.path.dirname(__file__), "static")
    template_path = os.path.join(os.path.dirname(__file__), "template")
    return tornado.web.Application([
        (r"/api/.+", taskConfig),
        (r"/.*", Index)
        # (r"/test", testPage.IndexHandler),
        # (r"/test/user", testPage.UserHandler),
        # (r"/socket/test", testPage.WebSocketHandler),
        # (r"/prince", princeSpa.princeIndex),
        # (r"^/prince/mock.+", princeSpa.princeMockMsg),
        # (r"/dy/getHourRank", princeSpa.getRankList),
        # (r"/socket/dy/flutter", flutterData.dyFlutterSocket),
        # (r"^/dy/flutter.+", flutterData.dyFlutter),
        # (r"^/dy/rn/gameCenter.+.+", rnGameCenter.dyReactNativeGameCenter),
        # (r"/upload", uploadFile.upload),
        # (r'/taskConfig', taskConfig)
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