import os
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, configure_mappers
from sqlalchemy_searchable import make_searchable
from sqlalchemy_searchable import search as sql_search

from database.services import init_services

class AppDB(object):

    def __init__(self, uri, metadata=None, engine_options=None, session_options=None, scopefunc=None, services=None):
        engine_options = engine_options or {}
        session_options = session_options or {}

        self.uri = uri

        self._engine = create_engine(self.uri, **engine_options)
        self.session_maker = sessionmaker(bind=self.engine, **session_options)
        self.session = scoped_session(self.session_maker, scopefunc=scopefunc)
                
        self.Model = declarative_base(metadata=metadata)  
        self.metadata.bind = self.engine
        
        configure_mappers()
        
        # setup services
        self._services = None
        self._register_services(services=services)        
    
    def drop_all(self):
        self.metadata.drop_all()   

    def create_all(self):
        self.metadata.create_all()

    @property
    def metadata(self):
        return self.Model.metadata

    @property
    def engine(self):
        return self._engine

    @property
    def query(self):
        return self.session.query

    def commit(self):
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise

    def _register_services(self, services=None):
        if self._services is None:
            self._services = services or init_services(self)
        return self._services

    @property
    def services(self):
        return self._services

    def search(self, query, *args, **kwargs):
        return sql_search(query, *args, **kwargs).all()
