import uuid
from datetime import datetime
from pycket.session import SessionMixin
import tornado.websocket
import tornado.web
import tornado.escape

from .main import BaseHandler

def make_data(handler,msg,username):
    chat = {
        'id':str(uuid.uuid4()),
        'body':msg,
        'username':username,
        'created':str(datetime.now()),
    }
    chat['html'] = tornado.escape.to_basestring(handler.render_string('message.html',chat=chat))
    print(chat)
    return chat

class RoomHandler(BaseHandler):
    """
    聊天室页面
    """
    @tornado.web.authenticated
    def get(self):

        self.render('room.html', messages=ChatWSHandler.history)


class ChatWSHandler(tornado.websocket.WebSocketHandler,SessionMixin):
    """
    处理和响应 Websocket 连接
    """
    waiters = set()   # 等待接受信息的用户
    history = []      # 存放历史消息
    history_size = 20 # 最后20条数据

    def get_current_user(self):
        return self.session.get('tudo_user',None)

    def open(self, *args, **kwargs):
        """ 新的 WebSocket 连接打开，自动调用"""
        print("new ws connecttion: {}".format(self))
        ChatWSHandler.waiters.add(self)

    def on_close(self):
        """ WebSocket连接断开，自动调用 """
        print("close ws connection: {}".format(self))
        ChatWSHandler.waiters.remove(self)

    def on_message(self, message):
        """ WebSocket 服务端接收到消息自动调用 """
        print("got message: {}".format(message))
        parsed = tornado.escape.json_decode(message)
        msg = parsed['body']
        chat = make_data(self,msg,self.current_user)
        self.update_history(chat)
        self.send_updates(chat)
        for w in ChatWSHandler.waiters:
            w.write_message(chat)
    def update_history(self,chat):
        # 把新消息更新到history，截取最后20条
        ChatWSHandler.history.append(chat['html'])
        if len(ChatWSHandler.history) > ChatWSHandler.history_size:
            ChatWSHandler.history = ChatWSHandler.history[-ChatWSHandler.history_size:]
#
    def send_updates(self,chat):
        # 给每个等待接收的用户发新的消息
        for w in ChatWSHandler.waiters:
            w.write_message(chat)



# class EchoWebSocket(tornado.websocket.WebSocketHandler):
#     def open(self):
#         print("WebSocket opened")
#
#     def on_message(self, message):
#         self.write_message(u"You said: " + message)
#
#     def on_close(self):
#         print("WebSocket closed")