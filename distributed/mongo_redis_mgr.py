# -*- coding: utf8 -*-
#user:gzf

from datetime import timedelta
from pymongo import MongoClient
from pymongo import IndexModel, ASCENDING, DESCENDING
import redis
import hashlib
import datetime

class MongoRedisUrlManager:
    def __init__(self, server_ip='localhost', client=None, expires=timedelta(days=30)):
        self.client = MongoClient(server_ip, 27017) if client is None else client
        self.redis_client = redis.StrictRedis(host=server_ip, port=6379, db=0)

        #create collection to store result
        self.db = self.client.spider

        #create index if db is empty
        if self.db.locations.count() is 0:
            self.db.locations.create_index([('status', ASCENDING)])

    #url出队
    def dequeueUrls(self, size=10):
        records = self.db.locations.find({'status':'new'}).limit(size)

        ids = []
        urls = []
        for record in records:
            ids.append(record['_id'])
            urls.append(record['url'])

        self.db.locations.update(
            {
                '_id': {'$in': ids}
            },
            {
                '$set': {'status': 'downloading'}
            }
        )

        if records is None:
            return None
        else:
            return urls

    #url入队
    def enqueueUrls(self, urls, status='new'):
        for url in urls:
            num = self.redis_client.get(url)
            if num is not None:
                self.redis_client.set(url, int(num) + 1)
                return
            else:
                self.redis_client.set(url, 1)

            self.db.locations.insert({
                '_id': hashlib.md5(url.encode('utf-8')).hexdigest(),
                'url': url,
                'status': status,
                'queue_time': datetime.datetime.utcnow(),
            })

    def finishUrl(self, url):
        record = {'status': 'done', 'done_time': datetime.datetime.utcnow()}
        self.db.locations.update({'_id': hashlib.md5(url.encode('utf-8').hexdigest())}, {'$set': record}, upsert=False)

    def clear(self):
        self.redis_client.flushdb() # Delete all keys in the current database
        self.db.locations.drop() # Drop current collection


