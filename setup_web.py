from database import metadata
from database.app_db import AppDB

def setup_db():
    database_uri = 'postgres+psycopg2://dbadmin:admindb@localhost:5432/platform'
    db = AppDB(database_uri, metadata=metadata)
    db.drop_all()
    #db.create_all()

    #sumo_db.category.create_from_list(['food drink','restaurant','groceries','bakery','beauty spas','health fitness','salon','gym','travel','pets','retail'])
    
    #demo_user = sumo_db.user.add(email='demo@sumo.promo', password='demo', first_name='DEMO', last_name='DEMO')


if __name__ == '__main__':
    setup_db()
