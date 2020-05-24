import tornado, os, random, re, time, asyncio
from threading import Timer

files = {}

@tornado.web.stream_request_body
class upload(tornado.web.RequestHandler):
    save_name = None
    save_seek = 0
    pre_seek = 0

    def prepare(self):
        self.save_seek = int(self.get_query_argument('s'))
        self.save_name = os.path.join(os.path.dirname(__file__), 'static/file', self.get_query_argument('f'))
        if self.save_name not in files.keys():
            files[self.save_name] = open(self.save_name, 'wb+')

    def data_received(self, chunk):
        files[self.save_name].seek(self.save_seek)
        files[self.save_name].write(chunk)
        self.save_seek = self.save_seek + len(chunk)

    def post(self):
        if self.save_seek == int(self.get_query_argument('t')):
            files[self.save_name].close()
            del files[self.save_name]
            print('上传成功：' + self.save_name)
        self.write({ 'error': 0, 'size': self.save_seek })
        self.finish()