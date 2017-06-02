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

listing_collection_table = Table('listing_collection', metadata,
    Column('listing_id', GUID, ForeignKey('listing.id')),
    Column('collection_id', GUID, ForeignKey('collection.id'))
)

user_group_table = Table('user_group_table', metadata,
    Column('user_id', GUID, ForeignKey('user.id')),
    Column('group_id', GUID, ForeignKey('group.id'))
)

class User(Model, ModelMixin, TimestampMixin, UserMixin):

    __tablename__ = 'user'

    email = Column(String(255), unique=True, nullable=False)    
    _password = Column(String(255))

    name = Column(String(255), default='')
    profile_pic = Column(String(2048))
    social_accounts = Column(JSONB)
    
    listings = relationship('Listing', backref='creator')

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, password):
        self._password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(12)).decode('utf8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf8'), self._password.encode('utf8'))

class Collection(Model, ModelMixin, TimestampMixin):
    
    __tablename__ = 'collection'

    name = Column(String(255), nullable=False)
    public = Column(Boolean, default=False)
    creator_id = Column(GUID, ForeignKey('user.id'))
    users = relationship('User', secondary=user_collection_table, backref='collections')

class Listing(Model, ModelMixin, TimestampMixin):
    
    __tablename__ = 'listing'

    name = Column(String(255), nullable=False)
    url = Column(String(3000), nullable=False)
    listing_type = Column(String(50), default='rental')
    infos = Column(JSONB)

    creator_id = Column(GUID, ForeignKey('user.id'))
    collections = relationship('Collection', secondary=listing_collection_table, backref='listings')

class Group(Model, ModelMixin, TimestampMixin):
    
    __tablename__ = 'group'

    name = Column(String(255))
    users = relationship('User', secondary=user_group_table, backref='groups')
    messages = relationship('Message', backref='group')

class Message(Model, ModelMixin, TimestampMixin):
    
    __tablename__ = 'message'

    user_id = Column(GUID, ForeignKey('user.id'))
    group_id = Column(GUID, ForeignKey('group.id'))
    content = Column(UnicodeText)
