from tornado import web

class Application(web.Application):
    
    def __init__(self, settings):
        super(Application, self).__init__([], **settings)

    def add_service(self, service):
        if hasattr(self, service.name):
            raise RuntimeError('application already set up {} service'.format(service.name))
        setattr(self, service.name, service)

    def remove_service(self, name):
        delattr(self, name)
