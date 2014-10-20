#! /usr/bin/env python
# coding = utf-8

__author__ = 'jeff.yu'



import json
from common.tools import recursion_del_key

class QueryProducer(object):

    def __init__(self, query):
        self.query_str = query
        self.convert_to_object()

    def convert_to_object(self):
        try:
            self.query_object = json.loads(self.query_str)
        except Exception as e:
            self.query_object = self.query_str

    def get_group(self):
        return self.query_object.get('group')

    def get_data(self):
        return self.query_object.get('data')

    def get_page(self):
        return self.query_object.get('settings').get('pagination').get('page')

    def get_size(self):
        return self.query_object.get('settings').get('pagination').get('size')

    def get_filters(self):
        return self.query_object.get('filters').get('$and')

    def get_order_key(self):
        return self.query_object.get('sort')[0].get('orderBy')

    def get_topn_metricvalue(self):
        return self.query_object.get('topn').get('metricvalue')

    def get_topn_threshold(self):
        return self.query_object.get('topn').get('threshold')

    def get_reverse_order(self):
        old_order = self.query_object.get('sort')[0].get('order')
        old_order_pattern = '"order":{0}'.format(old_order)
        if old_order == 1:
            new_order = -1
        else:
            new_order = 1
        new_order_pattern = '"order":{0}'.format(new_order)
        return self.query_str.replace(old_order_pattern, new_order_pattern)

    def get_no_page_query(self):
        page = self.get_page()
        size = self.get_size()
        old_pagination = '"size":{0},"page":{1}'.format(size, page)
        new_pagination = '"size":10000,"page":0'
        return self.query_str.replace(old_pagination, new_pagination)

    def get_no_lp_query(self):
        """
        :return: query that remove process_type key and add filter which offer_id = -1
        """
        no_lp_query = recursion_del_key(self.query_object, 'process_type')
        no_lp_query['filters']['$and'] = {"offer_id":{"$eq":-1}}
        str_no_lp_query = json.dumps(no_lp_query).replace("'", '"').replace(', "', ',"')
        return str_no_lp_query

    def get_no_topn_query(self):

        orderItem = self.get_topn_metricvalue()
        sortMap = {}
        sortMap["orderBy"] = orderItem
        sortMap["order"] = -1
        self.query_object['sort'] = [sortMap]
        del self.query_object['topn']
        queryStr = json.dumps(self.query_object)
        return queryStr.replace("'", '"').replace(', "', ',"')

    def getNoFilterQuery(self):

        self.query_object['filters']['$and'] = {}
        queryStr = json.dumps(self.query_object)
        return queryStr.replace("'", '"').replace(', "', ',"').replace(": ", ":")


if __name__ == '__main__':
    qop = QueryProducer('{"settings":{"time":{"start":1404172800,"end":1412121600,"timezone":0},"data_source":"ymds_druid_datasource","report_id":"121212","pagination":{"size":1000000,"page":0}},"group":["screen_h", "sub2", "sub8", "offer_id", "year", "month", "week", "day"],"data":["click", "conversion"],"filters":{"$and":{"month": {"$eq": "Jul"}, "day": {"$neq": "2014-08-06"}, "year": {"$neq": "2014"}}},"sort":[]}')
    print qop.getNoFilterQuery()
