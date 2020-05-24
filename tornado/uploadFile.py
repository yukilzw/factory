import tornado, os, random, re

@tornado.web.stream_request_body
class upload(tornado.web.RequestHandler):
    save_name = None
    fileObj = None
    save_seek = 0

    def prepare(self):
        self.save_name = os.path.join(os.getcwd(), 'static', self.get_query_argument('name'))
        self.fileObj = open(self.save_name, 'wb+')

    def data_received(self, chunk):
        self.fileObj.seek(self.save_seek)
        self.fileObj.write(chunk)
        self.save_seek = self.save_seek + len(chunk)
        print(self.save_seek)

    def post(self):
        self.fileObj.close()
        data = { 'error': 0 }
        print('上传成功：' + self.save_name)
        self.write(data)