import logging
import ujson
from tornado import web, websocket

class BaseHandler(web.RequestHandler):
    
    @property
    def db(self):
        return self.application.db
    
    def prepare(self):
        logging.debug("PREPARE: SET DB SCOPE")
        self.db.scope.set(self)

    def on_finish(self):
        logging.debug("FINISH: SET DB SCOPE AND REMOVE SESSION")
        self.db.scope.set(self)
        self.db.session.remove()
        self.db.scope.set(None)

    def reply_error(self, status, error):
        self.set_status(status)
        logging.error(error)
        self.write('Error: {}'.format(error))
        self.finish()

    def get_post_data(self):
        try:
            data = ujson.loads(self.request.body)
            return data
        except Exception as e:
            self.reply_error(500, 'Error parsing POST data {}'.format(e))

class WebHandler(BaseHandler):

    def get_current_user(self):
        user_id = self.get_secure_cookie('app_user')
        if not user_id:
            return None
        return user_id.decode('utf-8')

    def set_current_user(self, user):
        self.clear_cookie('app_user')
        self.set_secure_cookie('app_user', str(user.id))


class WSHandler(websocket.WebSocketHandler):

    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user = self.get_secure_cookie('app_user')
        if not user:
            return None
        return user        
