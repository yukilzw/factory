# -*- coding: utf-8 -*-
# Mock data server,used for clients.
import os
import tornado.web
import tornado.websocket
import flutterData, rnGameCenter, uploadFile, princeSpa, testPage

current_path = os.path.dirname(__file__)

settings={
    "template_path": os.path.join(current_path, "template"),
    "static_path": os.path.join(current_path, "static"),
    # "static_url_prefix":"/static/",
    "debug": True,
    "cookie_secret": "__TODO:LIU_ZHAN_WEI"
}

class BaseHandler(tornado.web.StaticFileHandler):
    def write_error(self, status_code, **kwargs):
        self.finish({
            'error': {
                'code': status_code,
                'message': self._reason,
            }
        })

def create_server():
    return tornado.web.Application([
        (r"/test", testPage.IndexHandler),
        (r"/test/user", testPage.UserHandler),
        (r"/socket/test", testPage.WebSocketHandler),
        (r"/prince", princeSpa.princeIndex),
        (r"^/prince/mock.+", princeSpa.princeMockMsg),
        (r"/dy/getHourRank", princeSpa.getRankList),
        (r"/socket/dy/flutter", flutterData.dyFlutterSocket),
        (r"^/dy/flutter.+", flutterData.dyFlutter),
        (r"^/dy/rn/gameCenter.+.+", rnGameCenter.dyReactNativeGameCenter),
        (r"/upload", uploadFile.upload),
        (r"/(.*)", BaseHandler,
            {
                "path": os.path.join(current_path, "flutter_web_bundle"),
                "default_filename": "index.html"
            }
        ),
    ], **settings)

if __name__ == "__main__":
    app = create_server()
    #app.listen(1236)

    sockets = tornado.netutil.bind_sockets(1236)
    #tornado.process.fork_processes(0)
    server = tornado.httpserver.HTTPServer(app)
    server.add_sockets(sockets)
    print('tornado start.')

    tornado.ioloop.IOLoop.current().start()