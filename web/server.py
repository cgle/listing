import logging, signal, time
from tornado import ioloop, httpserver
import tornado.gen

# PATCHES
class Scope(object):
    
    def __init__(self):
        self._current_scope = None

    def set(self, scope):
        self._current_scope = scope

    def get(self):
        return self._current_scope

original_runner_init = tornado.gen.Runner.__init__
original_runner_run = tornado.gen.Runner.run
original_runner_handle_exception = tornado.gen.Runner.handle_exception

# GLOBAL SCOPE
global scope
scope = Scope()

def new_runner_init(self, *args, **kwargs):
    self.scope = scope.get()
    original_runner_init(self, *args, **kwargs)

def new_runner_run(self, *args, **kwargs):
    scope.set(self.scope)
    return original_runner_run(self, *args, **kwargs)

tornado.gen.Runner.__init__ = new_runner_init
tornado.gen.Runner.run = new_runner_run

def register_shutdown_handler(http_server):
    shutdown_handler = lambda sig, frame: shutdown(http_server)
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

def shutdown(http_server):
    ioloop_instance = ioloop.IOLoop.instance()
    logging.info('Stopping server gracefully.')

    http_server.stop()

    def finalize():
        ioloop_instance.stop()
        logging.info('Server stopped.')

    # wait for 0.5 second then stop io_loop
    ioloop_instance.add_timeout(time.time() + 0.1, finalize)


def setup_application(settings):
    logging.debug('SETUP APPLICATION')
    from web.core.app import Application
    app = Application(settings)

    logging.debug('SETUP SERVICES')
    from web.services.db import DBAppService
    from database import metadata
    db_service = DBAppService(settings['db']['uri'],
                              connection_string=settings['db']['connection_string'],
                              metadata=metadata, 
                              scope=scope, 
                              scopefunc=scope.get)
    app.add_service(db_service)
    from web.services.chat import ChatManager
    chat_manager = ChatManager(db_service)
    
    logging.debug('SETUP APP HANDLERS')
    app_handlers = []
    import web.handlers.site as site
    import web.handlers.auth as auth
    import web.handlers.chat as chat    

    app_handlers += [
        (r'/', site.IndexHandler),
        (r'/about', site.AboutHandler),
        (r'/contact', site.ContactHandler),
        (r'/tutorial', site.TutorialHandler),
        
        (r'/register', auth.RegisterHandler),
        (r'/login', auth.LoginHandler),
        (r'/logout', auth.LogoutHandler),

        (r'/ws/chat', chat.ChatWSHandler, dict(chat_manager=chat_manager)),
        (r'/chat-groups/add-user', chat.AddUserToChatGroupHandler),
        (r'/chat-groups/remove-user', chat.RemoveUserFromChatGroupHandler),
        (r'/chat-groups/get', chat.GetChatGroupsHandler),
        (r'/chat-groups/create', chat.CreateChatGroupHandler),
    ]
    
    app.add_handlers(r'.*', app_handlers)

    return app

def start(settings):
    app = setup_application(settings)
    http_server = httpserver.HTTPServer(app)
    http_server.listen(settings['port'], settings['host'])
    register_shutdown_handler(http_server)
    ioloop.IOLoop.current().start()
