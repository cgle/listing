import psycopg2
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from tornado import gen, ioloop, concurrent
from database.app_db import AppDB

class DBAppService(AppDB):
    
    name = 'db'
    executor = ThreadPoolExecutor(max_workers=16)
    
    def __init__(self, *args, **kwargs):
        self.scope = kwargs.pop('scope', None)
        self.connection_string = kwargs.pop('connection_string', None)
        super(DBAppService, self).__init__(*args, **kwargs)
        
        self.io_loop = ioloop.IOLoop.instance()

    @concurrent.run_on_executor
    def _execute(self, query, commit=False):
        conn = None
        try:
            conn = psycopg2.connect(self.connection_string)
            cur = conn.cursor()
            cur.execute(query)
                        
            if not commit:
                # query:
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()                
                return (columns, rows)
            else:
                conn.commit()                
        except Exception as e:
            if conn:
                conn.rollback()
            raise RuntimeError('Error DB execute query {}'.format(e))
        finally:
            if conn:
                conn.close()

        return (None, None)

    @gen.coroutine
    def save_messages(self, messages):
        messages = [str((m['user_id'], m['group_id'], m['content'])) for m in messages]

        q = '''
            INSERT INTO "message"
            (user_id,group_id,content)
            VALUES {}
        '''.format(','.join(messages))

        yield self._execute(q)
        return

    @gen.coroutine
    def get_messages_history(self, group_id, timestamp=datetime.utcnow(), limit=100):
        q = '''
            SELECT * FROM "message"
            WHERE group_id={} AND created_at < {} LIMIT {}
        '''.format(self.group_id, timestamp, limit)

        messages = yield self._execute(q)
        raise gen.Return(messages)
