__author__ = 'jeff.yu'

#! /usr/bin/env python
# --*-- coding : utf-8 --*--

import urllib2
import urllib
import json


def get_data(query_data):

    query_url = "http://172.20.0.70:8080/trading/report?"
    para_data = {"report_param":  query_data}
    post_data = urllib.urlencode(para_data)
    try:
        f = urllib2.build_opener().open(urllib2.Request(query_url, post_data), timeout = 60).read()
    except Exception as e:
        print 'Http Error, No data Get'
        exit(-1)

    format_data = None
    try:
        format_data = json.loads(f)['data']['data']
    except Exception as e:
        print 'Parser Response Data to Json Error'
        exit(-1)
    return format_data


if __name__ == '__main__':
    print get_data('{"settings":{"time":{"start":1404172800,"end":1409529600,"timezone":0},"data_source":"contrack_druid_datasource_ds","report_id":"121212","pagination":{"size":1000000,"page":0}},"group":["year","week","offer_id"],"data":["clicks","outs","ctr","cr","income","cost","convs","roi","net"],"filters":{"$and":{"offer_id":{"$eq":-1}}},"sort":[{"orderBy":"clicks","order":-1}]}')