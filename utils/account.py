import hashlib

from models.auth import User, Post


def hashed(text):
    return hashlib.md5(text.encode('utf8')).hexdigest()


def authenticate(username, password):
    # session = Session()
    # user = session.query(User).filter_by(name=username).first()

    return User.get_password(username) == hashed(password)


class HandlerORM:
    """
    辅助操作数据库的工具类，结合 RequestHandler 使用

    """
    def __init__(self, db_session):
        """

        :param db_session: 由 handler 进行实例化和 close
        """
        self.db = db_session

    def get_user(self, username):
        user = self.db.query(User).filter_by(name=username).first()
        return user

    def register(self, username, password):
        self.db.add(User(name=username, password=hashed(password)))
        self.db.commit()

    def add_post(self, image_url, thumb_url, username):
        user = self.get_user(username)
        post = Post(image_url=image_url, thumb_url=thumb_url, user=user)
        self.db.add(post)
        self.db.commit()
        post_id = post.id

        return post_id

    def Yget_all_posts(self):
        posts = self.db.query(Post).all()
        return posts

    def get_posts_for(self, username):
        user = self.get_user(username)
        posts = self.db.query(Post).filter_by(user=user).all()
        return posts

    def get_post(self, post_id):
        """
        返回特定 id 的 post 实例
        :param post_id:
        :return:
        """
        post = self.db.query(Post).filter_by(id=post_id).first()
        return post

    # def like_posts_for(self, username):
    #     """
    #     查询用户喜欢的 posts
    #     :param username:
    #     :return:
    #     """
    #     user = self.get_user(username)
    #     posts = self.db.query(Post).filter(Post.id == Like.post_id,
    #                                        Like.user_id == user.id,
    #                                        Post.user_id != user.id)
    #     return posts
    #
    # def count_like_for(self, post_id):
    #     count = self.db.query(Like).filter_by(post_id=post_id).count()
    #     return count