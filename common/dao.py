#! /usr/bin/env python
# --*-- coding:utf-8 --*--

__author__ = 'jeff.yu'


import pymongo
from ConfigParser import ConfigParser


class Pydbc(object):

    def __init__(self):
        self.getConfig()
        self.setConnection()
        self.clearCollection()

    def getConfig(self):
        parser = ConfigParser()
        parser.read('../config/dbconfig.ini')
        self.db_type = parser.get('database', 'db_type')
        self.db_host = parser.get('database', 'db_host')
        try:
            self.db_port = int(parser.get('database', 'db_port'))
        except Exception as e:
            print 'get db config[port] error, should be integer'
        self.db_name = parser.get('database', 'db_name')
        self.db_table = parser.get('database', 'db_table')

    def setConnection(self):
        self.conn = pymongo.Connection(self.db_host, self.db_port)
        self.db = eval('self.conn.{0}'.format(self.db_name))
        self.collection = eval('self.db.{0}'.format(self.db_table))

    def insertCollection(self, dataSet):
        for data in dataSet:
            self.collection.insert(data)
        return 0

    def queryCollection(self, queryFilter):
        queryFilterData = self.collection.find(queryFilter)
        returnData = []
        for data in queryFilterData:
            del data['_id']
            returnData.append(data)
        return returnData


    def clearCollection(self):
        self.collection.remove()


if __name__ == '__main__':
    pyDbc = Pydbc()
    pyDbc.insertCollection([{"AccountID":21,"UserName":"libing"}])
