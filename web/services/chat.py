from tornado import gen, ioloop, queues

class ChatGroup(object):
    
    def __init__(self, group_id, manager, buffer_size=500):
        self.io_loop = ioloop.IOLoop.instance()    
        self.group_id = group_id
        self.manager = manager
        self.active = True
        self.clients = set()
        
        self.buffer_size = buffer_size
        self.messages_buffer = []

    @property
    def db(self):
        return self.manager.db

    def add_client(self, client):
        self.clients.add(client)

    def remove_client(self, client):
        self.clients.remove(client)
    
    def new_message(self, message):
        if len(self.messages_buffer) <= self.buffer_size:
            self.messages_buffer.append(message)
        else:
            self.flush_messages_buffer()

        self.notify_clients(message)

    def notify_clients(self, message):
        for client in self.clients:
            client.send_new_message_update(message)
        
    @gen.coroutine
    def flush_messages_buffer(self):
        # reset messages_buffer
        messages, self.messages_buffer = self.messages_buffer, []
        yield self.db.save_messages(messages)

class ChatManager(object):
    
    name = 'chat_manager'

    def __init__(self, db):
        self.db = db
        self.groups = {}

    def add_or_get_group(self, group_id):
        if group_id not in self.groups:
            self.groups[group_id] = ChatGroup(group_id, self)
        return self.groups[group_id]

    def remove_group(self, group_id):
        del self.groups[group_id]
