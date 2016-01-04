import pymongo

from configs import dbconfig

__author__ = 'sunshine'


class MongodbUtil(object):
    def __init__(self, host=dbconfig.mongodb_host, port=dbconfig.mongodb_port, user=dbconfig.mongodb_user,
                 pwd=dbconfig.mongodb_pwd, db=dbconfig.mongodb_db):
        client = pymongo.MongoClient(host, port, connect=False)
        db = client[db]
        db.authenticate(user, pwd, source='admin')
        self.db = db
