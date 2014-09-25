__author__ = 'jeff.yu'

#! /usr/bin/env python
# coding = utf-8

import json

class QueryProducer(object):

    def __init__(self, query):
        self.query_str = query
        self.convert_to_object()

    def convert_to_object(self):
        try:
            self.query_object = json.loads(self.query_str)
        except TypeError as e:
            self.query_object = self.query_str

    def get_order_key(self):
        return self.query_object.get('sort')[0].get('orderBy')

    def get_reverse_order(self):
        old_order = self.query_object.get('sort')[0].get('order')
        old_order_pattern = '"order":{0}'.format(old_order)
        if old_order == 1:
            new_order = -1
        else:
            new_order = 1
        new_order_pattern = '"order":{0}'.format(new_order)
        return self.query_str.replace(old_order_pattern, new_order_pattern)


if __name__ == '__main__':
    print QueryProducer('{"settings":{"time":{"start":1404172800,"end":1409529600,"timezone":0},"data_source":"contrack_druid_datasource_ds","report_id":"121212","pagination":{"size":1000000,"page":0}},"group":["year","week","offer_id"],"data":["clicks","outs","ctr","cr","income","cost","convs","roi","net"],"filters":{"$and":{"offer_id":{"$eq":-1}}},"sort":[{"orderBy":"clicks","order":-1}]}').get_reverse_order()