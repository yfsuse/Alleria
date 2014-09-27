#! /usr/bin/env python
# --*-- coding = utf-8 --*--

__author__ = 'jeff.yu'




import sys
sys.path.append(sys.path[0].replace('/script', ''))


from base import Test
from common.parser import QueryProducer
import logging
import logging.config
from common.dataconv import conv_data


class PageTest(Test):

    def __init__(self, query, check_level = "low", islp = False):
        super(PageTest, self).__init__(query)
        self.check_level = check_level
        if islp:
            self.log_identifier = "pagelp"
        else:
            self.log_identifier = "page"
        logging.config.fileConfig("../config/logging.ini")
        self.logger = logging.getLogger("alleria")
        self.queryparser = QueryProducer(self.query)

    def get_split_data(self):
        split_size = self.queryparser.get_size()
        split_page = self.queryparser.get_page()
        split_range = slice(split_size * split_page, split_size * (split_page + 1))
        return self.http_data[1:][split_range]

    def __eq__(self, other):

        no_page_data = other.http_data
        no_page_data_len = len(no_page_data)
        page_data = self.http_data[1:]

        print no_page_data
        print page_data

        size = self.queryparser.get_size()
        page = self.queryparser.get_page()

        if page_data == []:
            if size * (page+1) > no_page_data_len:
                return True
            else:
                self.logger.error(""" [{0}] size * page >> total record count, should no result returned
                                       {1}""".format(self.log_identifier, self.query))
                return False


        if no_page_data_len == 0:
            self.logger.error(""" [{0}] no page, and return None
                                  {1}
                              """.format(self.log_identifier, other.query))
            return False

        page_data_converted = conv_data(self.http_data[1:], self.check_level)
        no_page_data_converted = conv_data(other.get_split_data(), self.check_level)

        if len(set(str(page_data_converted)) - set(str(no_page_data_converted))) == 0: # step 2: if data set not equals return false
            return True
        else:
            self.logger.error("""
                              [{0}] data set is not equal
                              {1}
                              """.format(self.log_identifier, self.query))
            return False

if __name__ == '__main__':
    case = '{"settings":{"time":{"start":1404201600,"end":1409558400,"timezone":0},"data_source":"contrack_druid_datasource_ds","report_id":"121212","pagination":{"size":8,"page":1}},"group":["mobile_brand_id"],"data":["clicks","outs","ctr","cr","income","cost","convs","roi","net"],"filters":{"$and":{}},"sort":[{"orderBy":"net","order":-1}]}'
    positive_case_result = PageTest(case)
    negative_case = QueryProducer(case).get_no_page_query()
    negative_case_result = PageTest(negative_case)
    if positive_case_result == negative_case_result:
        print "success"