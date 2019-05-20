import os
import time
from lxml import etree
from oil import oil
import hashlib
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.options import options, define

settings = {
    "debug": True,
    "template_path":"templates",
    "static_path":"static"
}

class MainHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def get(self):
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch("http://www.sinacloud.com")
        self.set_header('content-type', 'text/plain')
        self.write('Hello, World!')

class WechatHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        token = 'wxpy'
        signature = self.get_argument("signature")
        timestamp = self.get_argument("timestamp")
        nonce = self.get_argument("nonce")
        echostr = self.get_argument("echostr")
        with open(signature, 'w'):pass
        tmp = [token, timestamp, nonce]
        tmp.sort()
        tmp = "".join(tmp) # .encode('utf8')
        real_signature = hashlib.sha1(tmp.encode('utf8')).hexdigest()
        with open(real_signature, 'w'):pass
        if signature == real_signature:
            self.write(echostr)
        else:
            self.send_error('error')

    def post(self):
        data = '<xml>' + str(self.request.body).split('<xml>')[1].split('</xml>')[0] + '</xml>'
        xml = etree.fromstring(data)
        ToUserName = xml.find('ToUserName').text
        FromUserName = xml.find('FromUserName').text
        MsgType = xml.find('MsgType').text
        Content = xml.find('Content').text
        if MsgType == 'text' and len(Content) == 17:
            Content = oil(Content)
            self.render(
                'reply_text.xml',
                FromUserName=ToUserName,
                ToUserName=FromUserName,
                CreateTime=int(time.time()),
                Content=Content
            )

if __name__ == "__main__":
    app_root = os.path.dirname(__file__)
    templates_root = os.path.join(app_root, 'templates')
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/wxpy", WechatHandler),
        ], **settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(os.environ['PORT'], "0.0.0.0")
    tornado.ioloop.IOLoop.current().start()