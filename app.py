import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options
from handlers import main


define("port",default="8888",help="Listening port",type=int)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", main.IndexHandler),
            (r"/explore", main.ExploreHandler),
            (r"/post/(?P<post_id>[0-9]+)", main.PostHandler),
            # (r"/register",account.RegisterHandler),  # 注册
            # (r"/login", account.LoginHanlder),  # 登录

        ]

        settings = dict(
            debug=True,
            template_path="templates",
            static_path="statics",
            # xsrf_cookies=True,
            cookie_secret="fdasjofdsa-gfdsgdsafadsdfsd",
            pycket={
                'engine': 'redis',
                'storage': {
                    'host': '127.0.0.1',  # ip
                    'port': 6379,
                    'db_sessions': 10,
                    'max_connections': 2 ** 31,
                },
                'cookies': {
                    # 设置过期时间
                    'expires_days': 2,
                    # 'expires':None, #秒
                },
            },
            login_url="/login",
        )

        super().__init__(handlers,**settings)


if __name__ == "__main__":
    application = Application()
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
