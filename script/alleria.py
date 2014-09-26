#! /usr/bin/env python
# --*-- coding : utf-8 --*--

__author__ = 'jeff.yu'

import sys
sys.path.append(sys.path[0].replace('/script', ''))


from common.producer import *
from sort import SortTest
from page import PageTest
from common.parser import QueryProducer
from time import ctime, strftime, localtime


def run_sort(islp = False):

    case_list = get_sort_cases(islp)
    suffix = strftime("%Y-%m-%d-%H_%M_%S", localtime())

    if islp:
        error_log = '../log/sortlp.error.log.{0}'.format(suffix)
        success_log = '../log/sortlp.success.log.{0}'.format(suffix)
    else:
        error_log = '../log/sort.error.log.{0}'.format(suffix)
        success_log = '../log/sort.success.log.{0}'.format(suffix)

    err_handler = open(error_log, 'w')
    suc_handler = open(success_log, 'w')
    count = 0
    for case in case_list[:50]:
        positive_case_result = SortTest(case)
        negative_case = QueryProducer(case).get_reverse_order()
        negative_case_result = SortTest(negative_case)
        if negative_case_result == positive_case_result:
            suc_handler.writelines(case + '\n')
        else:
            err_handler.writelines(case + '\n')
        count += 1
        print ctime() + " run sort case at : ", count
    err_handler.close()
    suc_handler.close()


def run_page(islp = False):

    case_list = get_page_cases(islp)
    suffix = strftime("%Y-%m-%d-%H_%M_%S", localtime())

    if islp:
        error_log = '../log/pagelp.error.log.{0}'.format(suffix)
        success_log = '../log/pagelp.success.log.{0}'.format(suffix)
    else:
        error_log = '../log/page.error.log.{0}'.format(suffix)
        success_log = '../log/page.success.log.{0}'.format(suffix)

    err_handler = open(error_log, 'w')
    suc_handler = open(success_log, 'w')
    count = 0
    for case in case_list[:50]:
        negative_case_result = PageTest(case)
        positive_case = QueryProducer(case).get_no_page_query()
        positive_case_result = PageTest(positive_case)
        if negative_case_result == positive_case_result:
            suc_handler.writelines(case + '\n')
        else:
            err_handler.writelines(case + '\n')
        count += 1
        print ctime() + " run page case at : ", count
    err_handler.close()
    suc_handler.close()

if __name__ == '__main__':
    run_sort(islp=True)
    run_sort()
    run_page()
    run_page(islp=True)


