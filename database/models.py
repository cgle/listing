import bcrypt
from datetime import datetime, timedelta
from sqlalchemy import Table, Column, String, ForeignKey, DateTime, Float, UnicodeText, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.hybrid import hybrid_property

from database import Model, metadata
from database.mixins import ModelMixin, TimestampMixin, UserMixin
from database.types import GUID

user_collection_table = Table('user_collection', metadata,
    Column('user_id', GUID, ForeignKey('user.id')),
    Column('collection_id', GUID, ForeignKey('collection.id'))
)

item_collection_table = Table('item_collection', metadata,
    Column('item_id', GUID, ForeignKey('item.id')),
    Column('collection_id', GUID, ForeignKey('collection.id'))
)

user_group_table = Table('user_group', metadata,
    Column('user_id', GUID, ForeignKey('user.id')),
    Column('group_id', GUID, ForeignKey('group.id'))
)

class User(Model, ModelMixin, TimestampMixin, UserMixin):

    __tablename__ = 'user'

    email = Column(String(255), unique=True, nullable=False)    
    _password = Column(String(255))

    name = Column(String(255), default='')
    profile_pic = Column(String(2048))
    is_active = Column(Boolean, default=True)
    is_online = Column(Boolean, default=True)
    social_accounts = Column(JSONB)
    
    items = relationship('Item', backref='creator')

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, password):
        self._password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(12)).decode('utf8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf8'), self._password.encode('utf8'))

#####################
# ITEM - COLLECTION #
#####################

class Collection(Model, ModelMixin, TimestampMixin):
    
    __tablename__ = 'collection'

    name = Column(String(255), nullable=False)
    is_public = Column(Boolean, default=False)
    creator_id = Column(GUID, ForeignKey('user.id'))
    users = relationship('User', secondary=user_collection_table, backref='collections')

class Item(Model, ModelMixin, TimestampMixin):
    
    __tablename__ = 'item'

    name = Column(String(255), nullable=False)
    url = Column(String(3000), nullable=False)
    item_type = Column(String(50), default='rental')
    infos = Column(JSONB)

    creator_id = Column(GUID, ForeignKey('user.id'))
    collections = relationship('Collection', secondary=item_collection_table, backref='items')

################
# CHAT MODELS  # 
################

class Group(Model, ModelMixin, TimestampMixin):
    
    __tablename__ = 'group'

    name = Column(String(255), nullable=False)
    creator_id = Column(GUID, ForeignKey('user.id'))
    is_public = Column(Boolean, default=False)
    members = relationship('User', secondary=user_group_table, backref='groups')

class Message(Model, ModelMixin, TimestampMixin):
    
    __tablename__ = 'message'

    user_id = Column(GUID, ForeignKey('user.id'))
    group_id = Column(GUID, ForeignKey('group.id'))
    content = Column(UnicodeText)
    group = relationship('Group')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'group_id': self.group_id,
            'content': self.content,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

