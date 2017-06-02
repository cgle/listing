from sqlalchemy import and_
import database.models as models

class DBService(object):

    name = None
    Model = None

    def __init__(self, db):
        self.db = db

        if hasattr(db, self.name):
            raise AttributeError('service {} exists in db'.format(self.name))

        setattr(db, self.name, self)

    def query(self):
        return self.db.query(self.Model)

    def add(self, **kwargs):
        item = self.Model(**kwargs)
        self.db.session.add(item)
        self.db.commit()
        return item
    
    def get_all(self, limit=100):
        return self.db.query(self.Model).limit(limit).all()
    
    def get_or_create(self, **kwargs):
        items = self.filter_by(**kwargs)
        if items:
            return items[0]
        else:
            return self.add(**kwargs)

    def filter(self, *args, **kwargs):
        limit = kwargs.pop('limit', None)
        filter_rule = and_(*args)
        return self.db.query(self.Model).filter(filter_rule).limit(limit).all()

    def filter_q(self, *args):
        filter_rule = and_(*args)
        return self.db.query(self.Model).filter(filter_rule)

    def filter_by(self, **kwargs):
        limit = kwargs.pop('limit', None)
        return self.db.query(self.Model).filter_by(**kwargs).limit(limit).all()

    def get_by_id(self, id):
        return self.db.query(self.Model).get(id)

    def update_by_id(self, id, **kwargs):
        item = self.db.query(self.Model).get(id)
        if item is None:
            raise RuntimeError('{} {} not found'.format(self.model.__name__, id))
        item.update(**kwargs)
        self.db.commit()
        return item

    def delete_by_id(self, id):
        item =self.db.query(self.Model).get(id)
        if item is None:
            raise RuntimeError('{} {} not found'.format(self.model.__name__, id))
        self.db.session.delete(item)
        self.db.commit()
    
    def update_one(self, item, **kwargs):
        item.update(**kwargs)
        self.db.commit()
        return item

    def delete_one(self, item):
        self.db.session.delete(item)
        self.db.commit()

    def search(self, *args, **kwargs):
        query = self.db.query(self.Model)
        return self.db.search(query, *args, **kwargs)

class UserService(DBService):
    
    name = 'user'
    Model = models.User

    def get_user_by_email(self, email):
        return self.db.query(models.User).filter_by(email=email).first()

    def update_by_email(self, email, **kwargs):
        user = self.get_user_by_email(email)
        if not user:
            raise RuntimeError('User {} not found'.format(email))

        user.update(**kwargs)
        self.db.commit()
        return user
    
    def delete_by_email(self, email):
        user = self.get_user_by_id(email)
        if not user:
            raise RuntimeError('User {} not found'.format(email))

        self.db.session.delete(user)
        self.db.commit()

class CollectionService(DBService):
    
    name = 'collection'
    Model = models.Collection

class ListingService(DBService):
    
    name = 'listing'
    Model = models.Listing

class GroupService(DBService):
    
    name = 'group'
    Model = models.Group

class MessageService(DBService):
    
    name = 'message'
    Model = models.Message

def init_services(db):

    services = {service.name: service for service in (
        UserService(db),
        CollectionService(db),
        ListingService(db),
        GroupService(db),
        MessageService(db),
    )}
    
    return services
