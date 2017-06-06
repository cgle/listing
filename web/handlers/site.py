from tornado import web
from web.core.handler import WebHandler

class IndexHandler(WebHandler):
    
    @web.authenticated
    def get(self):
        groups = self.db.group.get_groups_by_user(self.current_user)
        default_group = None if not groups else groups[0]
        return self.render('index.html', groups=groups, default_group=default_group)

class AboutHandler(WebHandler):
    
    def get(self):
        return self.render('about.html')

class ContactHandler(WebHandler):
    
    def get(self):
        return self.render('contact.html')

class TutorialHandler(WebHandler):
    
    def get(self):
        return self.render('tutorial.html')
