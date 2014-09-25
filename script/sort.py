#! /usr/bin/env python
# --*-- coding:utf-8 --*--

__author__ = 'jeff.yu'


from common.parser import QueryProducer
from base import Test
import logging
import logging.config
from common.dataconv import conv_data
import sys
sys.path.append(sys.path[0].replace('\script', ''))



class SortTest(Test):

    def __init__(self, query, check_level = "low"):
        logging.config.fileConfig("../config/logging.ini")
        self.logger = logging.getLogger("alleria")
        self.check_level = check_level
        super(SortTest, self).__init__(query)

    def get_orderdata_list(self):
        orderBy = QueryProducer(self.query).get_order_key()
        order_index = self.http_data[0].index(orderBy)
        orderdata = []
        for dataset in self.http_data[1:]:
            orderdata.append(dataset[order_index])
        return orderdata

    def __eq__(self, other):

        if self.http_len_data == 0 or other.http_len_data == 0:
            self.logger.debug('sort - data set is null: {0}'.format(self.query))
            return False


        if self.http_len_data == other.http_len_data:
            if len(set(str(self.http_data)) - set(str(other.http_data))) == 0: # if not str() then unhashable type: 'list' raised
                reverse_data = other.get_orderdata_list()
                reverse_data.reverse()
                order_data_list = self.get_orderdata_list()
                if conv_data(order_data_list, self.check_level) == conv_data(reverse_data, self.check_level):
                    return True
                else:
                    self.logger.debug("""sort - the content of data not equal: {0}
                                                                     {1}\n\n""".format(order_data_list, reverse_data))
                    return False
            else:
                self.logger.debug('sort - data set not equal')
                return False
        else:
            self.logger.debug('sort - data len not equal')
            return False

if __name__ == '__main__':
    query = '{"settings":{"time":{"start":1404172800,"end":1409529600,"timezone":0},"data_source":"contrack_druid_datasource_ds","report_id":"121212","pagination":{"size":1000000,"page":0}},"group":["year","week","offer_id"],"data":["clicks","outs","ctr","cr","income","cost","convs","roi","net"],"filters":{"$and":{"offer_id":{"$eq":-1}}},"sort":[{"orderBy":"clicks","order":-1}]}'
    reverse_query = QueryProducer(query).get_reverse_order()
    query_obj = SortTest(query)
    reverse_query_obj = SortTest(reverse_query)
    if query_obj == reverse_query_obj:
        print "equal"