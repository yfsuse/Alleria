#! /usr/bin/env python
# --*-- coding : utf-8 --*--

__author__ = 'jeff.yu'


from itertools import combinations
from random import choice, randint
from common.tools import mutichoice, makeDayList


TRADINGDESK_GROUP = ("device_id", "os_id", "mobile_brand_id", "carrier_id", "screen_w", "screen_h", "ref_site", "site", "brand_id", "model_id",
                "country_id", "city_id", "state_id",
                "sub1","sub2","sub3","sub4","sub5","sub6","sub7","sub8",
                "hour", "day", "week", "month",
                "offer_id")
YEAHMOBI_GROUP = ["aff_id","aff_manager","aff_sub1","aff_sub2","aff_sub3","aff_sub4","aff_sub5","aff_sub6","aff_sub7","aff_sub8","adv_id","adv_manager","adv_sub1","adv_sub2","adv_sub3","adv_sub4","adv_sub5","adv_sub6","adv_sub7","adv_sub8","offer_id","currency","rpa","cpa","ref_track","ref_track_site","ref_conv_track","click_ip","conv_ip","transaction_id","click_time","conv_time","time_diff","user_agent","browser","device_brand","device_model","device_os","device_type","country","time_stamp","log_tye","visitor_id","x_forwarded_for","state","city","isp","mobile_brand","platform_id","screen_width","screen_height","type_id","conversions","track_type","session_id","visitor_node_id","expiration_date","is_unique_click","gcid","gcname","browser_name","device_brand_name","device_model_name","platform_name","device_type_name","os_ver_name","os_ver"]


COMMON_DATA = ("clicks","outs","ctr","cr","income","cost","convs","roi","net")
YEAR_LIST = ["2013", "2014"]
MONTH_LIST = ["Jul", "Aug", "Sep"]
WEEK_LIST = ["Jul-1", "Jul-2", "Jul-3", "Jul-4", "Aug-1", "Aug-2", "Aug-3", "Aug-4", "Sep-1", "Sep-2", "Sep-3"]
DAY_LIST = makeDayList(2014, 2015, 7, 10, 1)
OPERATOR_LIST = ["$eq", "$neq"]
MAX_GROUP_SELECTED = 5

QUERY_TEMPLATE = '{"settings":{"time":{"start":1404201600,"end":1409558400,"timezone":0},"data_source":"contrack_druid_datasource_ds","report_id":"121212","pagination":{"size":1000000,"page":0}},"group":%s,"data":["clicks","outs","ctr","cr","income","cost","convs","roi","net"],"filters":{"$and":{}},"sort":[{"orderBy":"%s","order":-1}]}'
TIMEFILTERS_TEMPLATE = '{"settings":{"time":{"start":1404172800,"end":1412121600,"timezone":0},"data_source":"ymds_druid_datasource","report_id":"121212","pagination":{"size":1000000,"page":0}},"group":%s,"data":["click", "conversion"],"filters":{"$and":%s},"sort":[]}'

def get_groups(groupName):

    total_group = []
    for count in xrange(1, MAX_GROUP_SELECTED): # max group 5
        mutli_group = combinations(groupName, count)
        for single_group in mutli_group:
            total_group.append(list(single_group))
    return total_group

def get_order():

    return choice(COMMON_DATA)

def get_page():

    return choice(range(1, 10))

def get_size():

    return choice(range(1, 10))

def get_sort_cases(islp = False):

    case_list = []

    if islp:
        old_pattern = '"contrack_druid_datasource_ds","report_id"'
        new_pattern = '"contrack_druid_datasource_ds","process_type":"lp","report_id"'
        REF_QUERY_TEMPLATE = QUERY_TEMPLATE.replace(old_pattern, new_pattern)
    else:
        REF_QUERY_TEMPLATE =  QUERY_TEMPLATE
    group_combinations = get_groups(TRADINGDESK_GROUP)
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
        old_pattern = '"filters":{"$and":{}},"sort"'
        new_pattern = '"filters":{"$and":{}},"sort"'
        REF_QUERY_TEMPLATE = QUERY_TEMPLATE.replace(old_pattern, new_pattern)
    else:
        REF_QUERY_TEMPLATE =  QUERY_TEMPLATE
    group_combinations = get_groups(TRADINGDESK_GROUP)
    for group in group_combinations:
        old_pagination = '"size":1000000,"page":0'
        new_pagination = '"size":{0},"page":{1}'.format(get_size(), get_page())
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

def get_lp_case():
    case_list = []
    group_combinations = get_groups(TRADINGDESK_GROUP)
    for group in group_combinations:
        old_pattern = '"contrack_druid_datasource_ds","report_id"'
        lp_pattern = '"contrack_druid_datasource_ds", "process_type":"lp", "report_id"'
        query_str = QUERY_TEMPLATE.replace(old_pattern, lp_pattern)
        # remove orderby pattern
        be_remove = ',"sort":[{"orderBy":"%s","order":-1}]'
        if group.count('offer_id') == 0:
            group.append('offer_id')
        query_str = query_str.replace(be_remove, '') % (group)
        query_str = query_str.replace("'", '"')
        case_list.append(query_str)
    return case_list

def get_topn_case():

    case_list = []
    group_combinations = get_groups(TRADINGDESK_GROUP)
    for group in group_combinations:
        islp = choice((False, False))
        old_pattern = '"net"],"filters"'
        lp_pattern = '"net"],"topn":{"metricvalue":"%s","threshold":%d},"filters"' % (choice(COMMON_DATA), choice(range(1, 100)))
        query_str = QUERY_TEMPLATE.replace(old_pattern, lp_pattern)
        # remove orderby pattern
        be_remove = ',"sort":[{"orderBy":"%s","order":-1}]'
        if islp:
            query_str = query_str.replace('"contrack_druid_datasource_ds","report_id"',
                                          '"contrack_druid_datasource_ds", "process_type":"lp", "report_id"')
            if group.count('offer_id') == 0:
                group.append('offer_id')
        else:
            if len(group) > 1:
                continue
            else:
                if group.count('year') == 1 or group.count('month') == 1 or group.count('day') == 1 or group.count('week') == 1 or group.count('hour') == 1:
                    continue
        query_str = query_str.replace(be_remove, ',"sort":[]') % (group)
        query_str = query_str.replace("'", '"')
        print query_str
        case_list.append(query_str)
    return case_list


def get_timeselect_case():

    case_list = []
    group_combinations = get_groups(YEAHMOBI_GROUP)
    for group in group_combinations:
        timeGroup = mutichoice(('year','month','week','day','hour'))
        if group.count('year') == 0 and group.count('month') == 0 and group.count('week') == 0 and group.count('day') == 0 and group.count('hour') == 0:
            group.extend(timeGroup)
            filterContent = {}
            for i in range(randint(1, len(timeGroup))):
                filter_item = choice(timeGroup)
                filter_operator = choice(OPERATOR_LIST)
                if filter_item == 'year':
                    filter_value = choice(YEAR_LIST)
                elif filter_item == 'month':
                    filter_value = choice(MONTH_LIST)
                elif filter_item == 'week':
                    filter_value = choice(WEEK_LIST)
                elif filter_item == 'day':
                    filter_value = choice(DAY_LIST)
                else:
                    filter_value = choice(str(randint(0, 23)))
                filterContent[filter_item] = {filter_operator:filter_value}
                query_str = TIMEFILTERS_TEMPLATE % (group, filterContent)
                queryStr = query_str.replace("'", '"').replace(": ", ":").replace(", ", ",")
                case_list.append(queryStr)
    return case_list


if __name__ == '__main__':
    pass
    get_topn_case()
    # sort_cases = get_sort_cases(islp=True)[:5]
    # for case in sort_cases:
    #     print case
    # get_page_cases()
    # print get_topn_case()
    # print get_timeselect_case()
