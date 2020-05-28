from .main import BaseHandler
from utils.account import authenticate


class RegisterHandler(BaseHandler):
    def get(self):
        self.render('register.html')


    def post(self):
        username = self.get_argument('username', '')
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')

        if username and password1 and (password1 == password2):
            self.orm.register(username, password1)
            self.session.set('tudo_user', username)
            self.redirect('/')
        else:
            self.write('bad username/password')


class LoginHanlder(BaseHandler):
    def get(self):
        next_url = self.get_argument('next', '')
        msg = self.get_argument('msg', '')
        self.render('login.html', next_url=next_url, msg=msg)
#
    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        next_url = self.get_argument('next', '')

        if not username.strip() or not password.strip():
            self.redirect('/login?msg=empty password or name')
        else:
            if authenticate(username, password):
                self.session.set("tudo_user", username)
                if next_url:
                    self.redirect(next_url)
                else:
                    self.redirect('/')
            else:
                self.redirect('/login?msg=password error')
#

class LogoutHandler(BaseHandler):
    def get(self):
        self.session.delete("tudo_user")
        self.render('logout.html')