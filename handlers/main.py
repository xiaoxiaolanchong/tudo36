import tornado.web
from pycket.session import SessionMixin
from PIL import Image
from utils.account import HandlerORM
from utils.photo import UploadImage
from models.db import Session


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('tudo_user', None)

    def prepare(self):
        self.db_session = Session()
        print('db session instance')
        self.orm = HandlerORM(self.db_session)

    def on_finish(self):
        self.db_session.close()
        print('db session close')


class IndexHandler(BaseHandler):
    """
    首页，用户上传图片的展示
    """
    # @tornado.web.authenticated
    def get(self):
        posts = self.orm.get_posts_for(self.current_user)
        self.render('index.html',posts=posts)


class ExploreHandler(BaseHandler):
    """
    最近上传的缩略图片页面
    """
    def get(self):
        posts = self.orm.get_all_posts()
        self.render('explore.html',posts=posts)


class PostHandler(BaseHandler):
    """
    单个图片详情页面
    """
    def get(self, post_id):
        post = self.orm.get_post(post_id)
        print('post return')
        if not post:
            self.write('wrong id {}'.format(post_id))
        else:
        #     count = self.orm.count_like_for(post_id)
        #     self.render('post.html', post=post, count=count)
            self.render('post.html',post_id=post_id,post=post)

#
# class ProfileHandler(BaseHandler):
#     """
#     用户的档案页面
#     """
#     @tornado.web.authenticated
#     def get(self):
#         name = self.get_argument('name', None)
#         if not name:
#             name = self.current_user
#         user = self.orm.get_user(name)
#         if user:
#             like_posts = self.orm.like_posts_for(name)
#             self.render('profile.html', user=user, like_posts=like_posts)
#         else:
#             self.write('user error')
#
#
class UploadHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('upload.html')

    @tornado.web.authenticated
    def post(self):
        pics = self.request.files.get('picture', [])
        post_id = 1
        for p in pics:
            # save_path = 'statics/upload/{}'.format(p['filename'])
            # with open(save_path,'wb') as f:
            #     f.write(p['body'])
            # post_id = self.orm.add_post('upload/{}'.format(p['filename']),None,self.current_user)
            # im = Image.open(save_path)
            # im.thumbnail((200,200))
            # im.save('statics/upload/thumd_{}.jpg'.format(p['filename']),'JPEG')
            up_img = UploadImage(p['filename'], self.settings['static_path'])
            up_img.save_upload(p['body'])
            up_img.make_thumb()
            post_id = self.orm.add_post(up_img.image_url,
                                        up_img.thumb_url,
                                        self.current_user)

        self.redirect('/post/{}'.format(post_id))
