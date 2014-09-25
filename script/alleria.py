#! /usr/bin/env python
# --*-- coding : utf-8 --*--

__author__ = 'jeff.yu'
from common.producer import *
from sort import SortTest
from page import PageTest
from common.parser import QueryProducer


def run_sort(islp = False):

    case_list = get_sort_cases(islp)
    err_handler = open('../log/sort.error.log', 'w')
    suc_handler = open('../log/sort.success.log', 'w')
    count = 0
    for case in case_list[:1]:
        positive_case_result = SortTest(case)
        negative_case = QueryProducer(case).get_reverse_order()
        negative_case_result = SortTest(negative_case)
        if negative_case_result == positive_case_result:
            suc_handler.writelines(case + '\n')
        else:
            err_handler.writelines(case + '\n')
        count += 1
        print "run sort case at : ", count
    err_handler.close()
    suc_handler.close()


def run_page(islp = False):

    case_list = get_page_cases(islp)
    err_handler = open('../log/page.error.log', 'w')
    suc_handler = open('../log/page.success.log', 'w')
    count = 0
    for case in case_list[:5]:
        negative_case_result = PageTest(case)
        positive_case = QueryProducer(case).get_no_page_query()
        positive_case_result = PageTest(positive_case)
        if negative_case_result == positive_case_result:
            suc_handler.writelines(case + '\n')
        else:
            err_handler.writelines(case + '\n')
        count += 1
        print "run page case at : ", count
    err_handler.close()
    suc_handler.close()

if __name__ == '__main__':
    run_sort(islp=True)
    # run_page()


