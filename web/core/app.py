import logging
from tornado import web

from database.app_db import AppDB

class Application(web.Application):
    
    def __init__(self, scope, settings):
        logging.debug('INIT APPLICATION')
        super(Application, self).__init__([], **settings)
        
        # setup DB
        logging.debug('SETUP DATABASE')
        from database import metadata
        self.scope = scope
        self.db = AppDB(self.settings['db']['uri'], metadata=metadata, scopefunc=self.scope.get)        
