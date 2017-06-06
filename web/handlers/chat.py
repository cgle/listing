import ujson
from datetime import datetime
import copy
from tornado import web, gen
from web.core.handler import WebHandler, WSHandler
import uuid

class GetChatGroupsHandler(WebHandler):
    
    @web.authenticated
    def get(self):
        try:
            groups = self.db.group.get_groups_by_user(self.current_user)
            self.write(ujson.dumps({'groups': groups}))
            self.finish()
        except Exception as e:
            self.reply_error(500, e)

class CreateChatGroupHandler(WebHandler):
    
    @web.authenticated
    def post(self):
        data = self.get_post_data()
        group_name = data['group_name']
        creator_id = self.current_user
        try:
            self.db.group.create(creator_id, group_name)
        except Exception as e:
            raise
            self.reply_error(500, e)

class AddUserToChatGroupHandler(WebHandler):
    
    @web.authenticated
    def post(self):
        data = self.get_post_data()
        email = data['email']
        group_id = data['group_id']
        
        if not self.db.group.is_member(self.current_user, group_id):
            self.reply_error(500, 'current user is not the member of group {}'.format(group_id))

        try:
            self.db.group.add_user_by_email(email, group_id)
            self.write('success add {} to group {}'.format(email, group_id))
            self.finish()
        except Exception as e:
            self.reply_error(500, e)

class RemoveUserFromChatGroupHandler(WebHandler):
    
    @web.authenticated
    def post(self):
        data = self.get_post_data()
        user_id = data['user_id']
        group_id = data['group_id']

        try:
            self.db.group.remove_user_by_id(user_id, group_id)
            self.write('success remove {} from group {}'.format(user_id, group_id))
            self.finish()
        except Exception as e:
            self.reply_error(500, e)

class ChatWSHandler(WSHandler):
    
    def __init__(self, *args, **kwargs):
        self.chat_manager = kwargs.pop('chat_manager', None)
        super(ChatClientWSHandler, self).__init__(*args, **kwargs)

    def open(self):
        self.user_id = self.current_user
        self.group_id = self.get_argument('group_id', None)
        if not self.group_id:
            return self.on_close()

        self.group = self.chat_manager.add_or_get_group(group_id)
        self.group.add_client(self)
        
        self.send_history()

    def on_close(self):
        self.group.remove_client(self)
    
    def send(self, msg_type, data):
        data = ujson.dumps({
            'msg_type': msg_type,
            'data': data
        })
        self.write_message(data)
    
    @gen.coroutine
    def send_history(self, timestamp=None):
        messages = yield self.db.get_messages_history(self.group_id, limit=100, timestamp=timestamp)
        self.send('history', messages)
    
    def send_new_message_update(self, message):
        self.send('new_message_update', message.to_dict())

    def on_message(self, data):
        msg = ujson.loads(data)
        msg_type = msg['msg_type']
        data = msg['data']
        if msg_type == 'new_message':
            self.group.new_message(data)
        elif msg_type == 'get_history':
            timestamp = data['timestamp']
            yield self.send_history(timestamp=timestamp)
        else:
            raise RuntimeError('invalid message type {}'.format(msg_type))
