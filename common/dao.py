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
        if not queryFilterData:
            return returnData
        for data in queryFilterData:
            del data['_id']
            returnData.append(data)
        return returnData

    def clearCollection(self):
        self.collection.remove()


if __name__ == '__main__':
    pyDbc = Pydbc()
    pyDbc.insertCollection([{u'week': u'Jul-5', u'conversion': 0, u'aff_id': 6618, u'month': u'Jul', u'click': 50}, {u'week': u'Sep-1', u'conversion': 3, u'aff_id': 10689, u'month': u'Sep', u'click': 7}, {u'week': u'Jul-5', u'conversion': 187, u'aff_id': 19166, u'month': u'Jul', u'click': 2313}, {u'week': u'Sep-4', u'conversion': 0, u'aff_id': 0, u'month': u'Sep', u'click': 0}, {u'week': u'Sep-2', u'conversion': 0, u'aff_id': 0, u'month': u'Sep', u'click': 143}, {u'week': u'Sep-3', u'conversion': 1, u'aff_id': 90010563, u'month': u'Sep', u'click': 1}, {u'week': u'Sep-2', u'conversion': 0, u'aff_id': 65536, u'month': u'Sep', u'click': 19}, {u'week': u'Sep-4', u'conversion': 1, u'aff_id': 90010502, u'month': u'Sep', u'click': 1}, {u'week': u'Sep-4', u'conversion': 1, u'aff_id': 90010503, u'month': u'Sep', u'click': 1}, {u'week': u'Sep-3', u'conversion': 1, u'aff_id': 90010569, u'month': u'Sep', u'click': 1}, {u'week': u'Jul-5', u'conversion': 0, u'aff_id': 15464, u'month': u'Jul', u'click': 10}, {u'week': u'Jul-5', u'conversion': 7, u'aff_id': 2152, u'month': u'Jul', u'click': 74}, {u'week': u'Jul-5', u'conversion': 0, u'aff_id': 12266, u'month': u'Jul', u'click': 3}, {u'week': u'Sep-4', u'conversion': 2, u'aff_id': 90010504, u'month': u'Sep', u'click': 2}, {u'week': u'Jul-5', u'conversion': 4, u'aff_id': 13166, u'month': u'Jul', u'click': 14}, {u'week': u'Jul-5', u'conversion': 161, u'aff_id': 5876, u'month': u'Jul', u'click': 11486}, {u'week': u'Aug-3', u'conversion': 0, u'aff_id': 7478, u'month': u'Aug', u'click': 1}, {u'week': u'Sep-1', u'conversion': 67, u'aff_id': 90010587, u'month': u'Sep', u'click': 3049}, {u'week': u'Sep-1', u'conversion': 7, u'aff_id': 90010591, u'month': u'Sep', u'click': 17}, {u'week': u'Sep-3', u'conversion': 1, u'aff_id': 90010594, u'month': u'Sep', u'click': 1}, {u'week': u'Sep-4', u'conversion': 0, u'aff_id': 90010401, u'month': u'Sep', u'click': 14}, {u'week': u'Sep-2', u'conversion': 3, u'aff_id': 90010408, u'month': u'Sep', u'click': 32}, {u'week': u'Sep-2', u'conversion': 41, u'aff_id': 100009, u'month': u'Sep', u'click': 54}, {u'week': u'Sep-4', u'conversion': 6, u'aff_id': 90010407, u'month': u'Sep', u'click': 672350}, {u'week': u'Jul-5', u'conversion': 0, u'aff_id': 2698, u'month': u'Jul', u'click': 7}, {u'week': u'Jul-5', u'conversion': 0, u'aff_id': 19466, u'month': u'Jul', u'click': 6}, {u'week': u'Jul-5', u'conversion': 3, u'aff_id': 13196, u'month': u'Jul', u'click': 285}, {u'week': u'Jul-5', u'conversion': 242, u'aff_id': 20749, u'month': u'Jul', u'click': 40661}, {u'week': u'Sep-3', u'conversion': 0, u'aff_id': 90010605, u'month': u'Sep', u'click': 1}, {u'week': u'Jul-5', u'conversion': 0, u'aff_id': 14736, u'month': u'Jul', u'click': 1}, {u'week': u'Sep-2', u'conversion': 0, u'aff_id': 100019, u'month': u'Sep', u'click': 1}, {u'week': u'Sep-2', u'conversion': 1, u'aff_id': 90010549, u'month': u'Sep', u'click': 1}, {u'week': u'Sep-4', u'conversion': 2, u'aff_id': 100017, u'month': u'Sep', u'click': 2}, {u'week': u'Sep-4', u'conversion': 12, u'aff_id': 100018, u'month': u'Sep', u'click': 11}, {u'week': u'Sep-4', u'conversion': 7, u'aff_id': 100020, u'month': u'Sep', u'click': 6}, {u'week': u'Sep-2', u'conversion': 25, u'aff_id': 90010555, u'month': u'Sep', u'click': 20}, {u'week': u'Jul-5', u'conversion': 225, u'aff_id': 13208, u'month': u'Jul', u'click': 16876}, {u'week': u'Jul-5', u'conversion': 0, u'aff_id': 10266, u'month': u'Jul', u'click': 168}, {u'week': u'Jul-5', u'conversion': 14, u'aff_id': 21403, u'month': u'Jul', u'click': 48}, {u'week': u'Jul-5', u'conversion': 0, u'aff_id': 18076, u'month': u'Jul', u'click': 5}, {u'week': u'Sep-1', u'conversion': 0, u'aff_id': 0, u'month': u'Sep', u'click': 204}, {u'week': u'Sep-2', u'conversion': 1, u'aff_id': 10689, u'month': u'Sep', u'click': 2}, {u'week': u'Jul-5', u'conversion': 0, u'aff_id': 21407, u'month': u'Jul', u'click': 179}, {u'week': u'Jul-5', u'conversion': 0, u'aff_id': 10656, u'month': u'Jul', u'click': 4}, {u'week': u'Jul-5', u'conversion': 275, u'aff_id': 7328, u'month': u'Jul', u'click': 134037}, {u'week': u'Sep-3', u'conversion': 1, u'aff_id': 100100, u'month': u'Sep', u'click': 1}, {u'week': u'Jul-5', u'conversion': 1, u'aff_id': 12582, u'month': u'Jul', u'click': 138}, {u'week': u'Jul-5', u'conversion': 1, u'aff_id': 13616, u'month': u'Jul', u'click': 24}, {u'week': u'Sep-4', u'conversion': 1, u'aff_id': 90010577, u'month': u'Sep', u'click': 1}, {u'week': u'Jul-5', u'conversion': 0, u'aff_id': 20150, u'month': u'Jul', u'click': 11}, {u'week': u'Jul-5', u'conversion': 27, u'aff_id': 100031, u'month': u'Jul', u'click': 57638}, {u'week': u'Jul-5', u'conversion': 1082, u'aff_id': 100032, u'month': u'Jul', u'click': 106017}, {u'week': u'Sep-1', u'conversion': 1, u'aff_id': 10000037, u'month': u'Sep', u'click': 21}, {u'week': u'Jul-5', u'conversion': 0, u'aff_id': 13122, u'month': u'Jul', u'click': 17}, {u'week': u'Jul-5', u'conversion': 370, u'aff_id': 20803, u'month': u'Jul', u'click': 144624}, {u'week': u'Sep-1', u'conversion': 0, u'aff_id': 90010407, u'month': u'Sep', u'click': 10}, {u'week': u'Sep-3', u'conversion': 1, u'aff_id': 90010407, u'month': u'Sep', u'click': 1620785}, {u'week': u'Sep-3', u'conversion': 1, u'aff_id': 100008, u'month': u'Sep', u'click': 2}, {u'week': u'Sep-3', u'conversion': 0, u'aff_id': 100009, u'month': u'Sep', u'click': 4}, {u'week': u'Sep-2', u'conversion': 1, u'aff_id': 90010603, u'month': u'Sep', u'click': 1}, {u'week': u'Sep-1', u'conversion': 1013, u'aff_id': 90010408, u'month': u'Sep', u'click': 1016}, {u'week': u'Jul-5', u'conversion': 1, u'aff_id': 13002, u'month': u'Jul', u'click': 119}, {u'week': u'Sep-4', u'conversion': 1, u'aff_id': 90010477, u'month': u'Sep', u'click': 1}, {u'week': u'Jul-5', u'conversion': 0, u'aff_id': 15562, u'month': u'Jul', u'click': 4}, {u'week': u'Jul-5', u'conversion': 17, u'aff_id': 2126, u'month': u'Jul', u'click': 232}, {u'week': u'Sep-3', u'conversion': 0, u'aff_id': 100017, u'month': u'Sep', u'click': 1}, {u'week': u'Sep-1', u'conversion': 3212, u'aff_id': 100019, u'month': u'Sep', u'click': 3238}, {u'week': u'Sep-1', u'conversion': 2818, u'aff_id': 100018, u'month': u'Sep', u'click': 2812}, {u'week': u'Jul-5', u'conversion': 4, u'aff_id': 2130, u'month': u'Jul', u'click': 70}, {u'week': u'Jul-5', u'conversion': 3, u'aff_id': 6099, u'month': u'Jul', u'click': 338}, {u'week': u'Sep-4', u'conversion': 8, u'aff_id': 90010484, u'month': u'Sep', u'click': 6}, {u'week': u'Sep-4', u'conversion': 1, u'aff_id': 90010480, u'month': u'Sep', u'click': 1}, {u'week': u'Sep-1', u'conversion': 3973, u'aff_id': 100017, u'month': u'Sep', u'click': 3989}])
    queryFilter = {"week":{"$eq":"Aug-2"},"month":{"$eq":"Jul"}}
    print pyDbc.queryCollection(queryFilter)

