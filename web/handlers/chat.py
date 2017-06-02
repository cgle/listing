from core.handler import WSHandler

class ChatClientWSHandler(WSHandler):
    
    def __init__(self, *args, **kwargs):
        self.chat_manager = kwargs.pop('chat_manager', None)
        super(ChatClientWSHandler, self).__init__(*args, **kwargs)

    def open(self):
        group = self.get_argument('group', None)
    
    def on_close(self):
        pass

    def on_message(self):
        pass
