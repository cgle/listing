from tornado import web, gen
from web.core.handler import WebHandler
import ujson

class RegisterHandler(WebHandler):
    
    def get(self):
        if self.current_user:
            return self.redirect("/")                
        return self.render("register.html")
    
    def post(self):
        data = self.get_post_data()
        email = data['email'].lower()
        password = data['password']

        try:
            user = self.db.user.get_user_by_email(email)
            if user:
                self.clear_cookie('app_user')
                return self.redirect('/login')

            user = self.db.user.add(email=email, password=password)
            self.set_current_user(user)
            self.write('success registered')
            self.finish()
            return
        except Exception as e:
            self.reply_error(401, 'Unauthenticated error: {}'.format(e))                  

class LoginHandler(WebHandler):
    
    def get(self):
        if self.current_user:
            return self.redirect("/")
        return self.render("login.html")

    def post(self):    
        data = self.get_post_data()
        email = data['email'].lower()
        password = data['password']
        
        try:
            user = self.db.user.get_user_by_email(email)
            if not user:
                self.clear_cookie('app_user')
                return self.redirect('/login')
        
            self.set_current_user(user)
            self.write('success logged in')
            self.finish()
            return
        except Exception as e:
            self.reply_error(401, 'Unauthenticated error: {}'.format(e))

class LogoutHandler(WebHandler):
    
    @web.authenticated
    def get(self):
        self.clear_cookie("app_user")
        self.redirect(self.get_argument("next", "/"))
