#! /usr/bin/env python
# --*-- coding : utf-8 --*--

__author__ = 'jeff.yu'


from itertools import combinations
from random import choice


COMMON_GROUP = ("device_id", "os_id", "mobile_brand_id", "carrier_id", "screen_w", "screen_h", "ref_site", "site", "brand_id", "model_id",
                "country_id", "city_id", "state_id",
                "sub1","sub2","sub3","sub4","sub5","sub6","sub7","sub8",
                "hour", "day", "week", "month",
                "offer_id")
COMMON_DATA = ("clicks","outs","ctr","cr","income","cost","convs","roi","net")

MAX_GROUP_SELECTED = 5

QUERY_TEMPLATE = '{"settings":{"time":{"start":1404201600,"end":1409558400,"timezone":0},"data_source":"contrack_druid_datasource_ds","report_id":"121212","pagination":{"size":1000000,"page":0}},"group":%s,"data":["clicks","outs","ctr","cr","income","cost","convs","roi","net"],"filters":{"$and":{}},"sort":[{"orderBy":"%s","order":-1}]}'


def get_groups():

    total_group = []
    for count in xrange(1, MAX_GROUP_SELECTED): # max group 5
        mutli_group = combinations(COMMON_GROUP, count)
        for single_group in mutli_group:
            total_group.append(list(single_group))
    return total_group

def get_order():

    return choice(COMMON_DATA)

def get_page():

    return choice(range(0, 10))

def get_size():

    return choice(range(1, 50))

def get_sort_cases(islp = False):

    case_list = []

    if islp:
        old_pattern = '"contrack_druid_datasource_ds","report_id"'
        new_pattern = '"contrack_druid_datasource_ds","process_type":"lp","report_id"'
        REF_QUERY_TEMPLATE = QUERY_TEMPLATE.replace(old_pattern, new_pattern)
    else:
        REF_QUERY_TEMPLATE =  QUERY_TEMPLATE
    group_combinations = get_groups()
    for group in group_combinations:
        query_str = REF_QUERY_TEMPLATE % (group, get_order())
        query = query_str.replace("'", '"')
        if islp:
            if query.find("offer_id") != -1:
                pass
            else:
                query = query.replace('],"data"', ',"offer_id"],"data"')
        case_list.append(query)
    return case_list

def get_page_cases(islp = False):
    case_list = []
    if islp:
        old_pattern = '"contrack_druid_datasource_ds","report_id"'
        new_pattern = '"contrack_druid_datasource_ds","process_type":"lp","report_id"'
        REF_QUERY_TEMPLATE = QUERY_TEMPLATE.replace(old_pattern, new_pattern)
    else:
        REF_QUERY_TEMPLATE =  QUERY_TEMPLATE
    group_combinations = get_groups()
    for group in group_combinations:
        old_pagination = '"size":1000000,"page":0'
        new_pagination = '"size":{0},"page":{1}'.format(get_page(), get_size())
        query_str = REF_QUERY_TEMPLATE % (group, get_order())
        page_query_str = query_str.replace(old_pagination, new_pagination)
        query = page_query_str.replace("'", '"')
        if islp:
            if query.find("offer_id") != -1:
                pass
            else:
                query = query.replace('],"data"', ',"offer_id"],"data"')
        case_list.append(query)
    return case_list

if __name__ == '__main__':
    sort_cases = get_sort_cases(islp=True)[:5]
    for case in sort_cases:
        print case
    # get_page_cases()