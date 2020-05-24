# -*- coding: utf-8 -*-
# Mock data server,used for clients.
import os
import tornado.web
import tornado.websocket
import flutterData, rnGameCenter, uploadFile, princeSpa, testPage

def create_server():
    static_path = os.path.join(os.path.dirname(__file__), "static")
    template_path = os.path.join(os.path.dirname(__file__), "template")
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