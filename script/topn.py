#! /usr/bin/env python
# --*-- coding:utf-8 --*--

__author__ = 'jeff.yu'

from base import Test
from common.parser import QueryProducer
from common.http import get_data

class TopnTest(Test):

    def __init__(self, query):
        super(TopnTest, self).__init__(query)
        self.qop = QueryProducer(query)
        print self.query
        self.slice = self.qop.get_topn_threshold()

    def getNoTopnData(self):

        noTopnQuery = self.qop.get_no_topn_query()
        return get_data(noTopnQuery)

    def _compare(self):
        no_topn_data = self.getNoTopnData()
        topn_data = self.http_data
        if topn_data == no_topn_data[:self.slice]:
            return True
        else:
            return False

if __name__ == '__main__':
        tt = TopnTest('{"settings":{"time":{"start":1404172800,"end":1409529600,"timezone":0},"data_source":"contrack_druid_datasource_ds", "report_id":"121212","pagination":{"size":1000000,"page":0}},"group":["year","week","offer_id"],"topn":{"metricvalue":"clicks","threshold":10},"data":["clicks","outs","ctr","cr","income","cost","convs","roi","net"],"filters":{"$and":{}},"sort":[]}')
        tt._compare()