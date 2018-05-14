#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 今日头条新闻分类数据爬取

import requests
import json
import time
import random

'''
100 民生 故事 news_story
101 文化 文化 news_culture
102 娱乐 娱乐 news_entertainment
103 体育 体育 news_sports
104 财经 财经 news_finance
105 时政 新时代 nineteenth
106 房产 房产 news_house
107 汽车 汽车 news_car
108 教育 教育 news_edu 
109 科技 科技 news_tech
110 军事 军事 news_military
111 宗教 无，凤凰佛教等来源
112 旅游 旅游 news_travel
113 国际 国际 news_world
114 证券 股票 stock
115 农业 三农 news_agriculture
116 电竞 游戏 news_game
'''

g_cnns = [
[100, '民生 故事', 'news_story'],
[101, '文化 文化', 'news_culture'],
[102, '娱乐 娱乐', 'news_entertainment'],
[103, '体育 体育', 'news_sports'],
[104, '财经 财经', 'news_finance'],
# [105, '时政 新时代', 'nineteenth'],
[106, '房产 房产', 'news_house'],
[107, '汽车 汽车', 'news_car'],
[108, '教育 教育', 'news_edu' ],
[109, '科技 科技', 'news_tech'],
[110, '军事 军事', 'news_military'],
# [111 宗教 无，凤凰佛教等来源],
[112, '旅游 旅游', 'news_travel'],
[113, '国际 国际', 'news_world'],
[114, '证券 股票', 'stock'],
[115, '农业 三农', 'news_agriculture'],
[116, '电竞 游戏', 'news_game']
]

g_ua = 'Dalvik/1.6.0 (Linux; U; Android 4.4.4; MuMu Build/V417IR) NewsArticle/6.3.1 okhttp/3.7.0.2'


g_id_cache = {}
g_count = 0

def get_data(tup):
    global g_id_cache
    global g_count
    cid = tup[0]
    cname = tup[2]
    url = "http://it.snssdk.com/api/news/feed/v63/"

    t = int(time.time()/10000)
    t = random.randint(6*t, 10*t)
    querystring = {"category":cname,"concern_id":"6215497896830175745","refer":"1","count":"20","max_behot_time":t,"last_refresh_sub_entrance_interval":"1524907088","loc_mode":"5","tt_from":"pre_load_more","cp":"51a5ee4f38c50q1","plugin_enable":"0","iid":"31047425023","device_id":"51425358841","ac":"wifi","channel":"tengxun","aid":"13","app_name":"news_article","version_code":"631","version_name":"6.3.1","device_platform":"android","ab_version":"333116,297979,317498,336556,295827,325046,239097,324283,170988,335432,332098,325198,336443,330632,297058,276203,286212,313219,328615,332041,329358,322321,327537,335710,333883,335102,334828,328670,324007,317077,334305,280773,335671,319960,333985,331719,336452,214069,31643,332881,333968,318434,207253,266310,321519,247847,281298,328218,335998,325618,333327,336199,323429,287591,288418,260650,326188,324614,335477,271178,326588,326524,326532","ab_client":"a1,c4,e1,f2,g2,f7","ab_feature":"94563,102749","abflag":"3","ssmix":"a","device_type":"MuMu","device_brand":"Android","language":"zh","os_api":"19","os_version":"4.4.4","uuid":"008796762094657","openudid":"b7215ea70ca32066","manifest_version_code":"631","resolution":"1280*720","dpi":"240","update_version_code":"6310","_rticket":"1524907088018","plugin":"256"}

    headers = {
        'cache-control': "no-cache",
        'postman-token': "26530547-e697-1e8b-fd82-7c6014b3ee86",
        'User-Agent': g_ua
        }

    response = requests.request("GET", url, headers=headers, params=querystring)


    jj = json.loads(response.text)
    with open('toutiao_cat_data.txt', 'a') as fp:
        for item in jj['data']:
            item = item['content']
            item = item.replace('\"', '"')
            # print item
            # item = item.decode('utf-8')
            item = json.loads(item)
            kws = ''
            if item.has_key('keywords'):
                kws = item['keywords']
            
            if item.has_key('ad_id'):
                print 'ad'
            elif not item.has_key('item_id') or not item.has_key('title'):
                print 'bad'
            else:
                item_id = item['item_id']
                print  g_count, cid, cname, item['item_id'], item['title'], kws
                if g_id_cache.has_key(item_id):
                    print 'dulp'
                else:
                    g_id_cache[item_id] = 1
                    line = u"{}_!_{}_!_{}_!_{}_!_{}".format(item['item_id'], cid, cname, item['title'], kws)
                    line = line.replace('\n', '').replace('\r', '')
                    line = line + '\n'
                    fp.write(line.encode('utf-8'))
                    g_count += 1
    

def get_routine():
    global g_count
    with open('toutiao_cat_data.txt', 'r') as fp:
        ll = fp.readlines()
        g_count = len(ll)
        for l in ll:
            ww = l.split('_!_')
            item_id = int(ww[0])
            g_id_cache[item_id] = 1
        print 'load cache done, ', g_count

    while 1:
        time.sleep(10)
        for tp in g_cnns:
            get_data(tp)

get_routine()