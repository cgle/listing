import logging
import ujson
from tornado import web, websocket

class BaseHandler(web.RequestHandler):
    
    @property
    def db(self):
        return self.application.db
    
    def prepare(self):
        self.application.scope.set(self)

    def on_finish(self):
        self.application.scope.set(self)
        self.db.session.remove()
        self.application.scope.set(None)

    def reply_error(self, status, msg):
        self.set_status(status)
        logging.error(msg)
        self.write(msg)
        self.finish()

    def get_post_data(self):
        try:
            data = ujson.loads(self.request.body)
            return data
        except Exception as e:
            self.reply_error(500, 'Error parsing POST data {}'.format(e))

class WebHandler(BaseHandler):
    
    def get_current_user(self):
        user = self.get_secure_cookie('app_user')
        if not user:
            return None
        return user

class WSHandler(websocket.WebSocketHandler):
    pass
