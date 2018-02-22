# -*- coding: utf8 -*-
#user:gzf

from datetime import timedelta

from pymongo import MongoClient
from pymongo import IndexModel, ASCENDING, DESCENDING

class MongoManager(object):

    def __init__(self, server_ip='localhost', client=None, expires=timedelta(days=30)):
        '''
        :param server_ip:
        :param client:  mongo database client
        :param expires: timedelta of amount of time before a cache entry is considered expired
        '''
        #如果没有client就新连接一个
        self.client = MongoClient(server_ip, 27017) if client is None else client

        #创建一个collection存储爬取下来的内容
        self.db = self.client.spider

        #create index if db is empty
        if self.db.locations.count() is 0:
            self.db.locations.create_index([("status", ASCENDING)])

    def dequeueItems(self, size=10):
        records = self.db.find({'status':'new'}).limit(size)

        ids = []
        for record in records:
            ids.append(record['_id'])

        self.db.locations.update(
            {
                '_id': {'$in': ids}
            },
            {
                '$set': {'status': 'downloading'}
            }
        )


        if records:
            return records
        else:
            return None

    def finishItmes(self, ids):
        self.db.locations.update(
            {
                '_id': {'$in': ids}
            },
            {
                '$set': {'status': 'finish'}
            }
        )

    def clear(self):
        self.db.locations.drop()