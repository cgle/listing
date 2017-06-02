from tornado import web
from web.core.handler import WebHandler

class IndexHandler(WebHandler):
    
    @web.authenticated
    def get(self):
        return self.render('index.html')

class AboutHandler(WebHandler):
    
    def get(self):
        return self.render('about.html')

class ContactHandler(WebHandler):
    
    def get(self):
        return self.render('contact.html')

class TutorialHandler(WebHandler):
    
    def get(self):
        return self.render('tutorial.html')
