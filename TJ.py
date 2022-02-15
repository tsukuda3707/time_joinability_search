import numpy as np
import pandas as pd
import time
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import dateutil.parser
import random
import os
import time
import json
import glob
import collections as cl

def PTJ(query_csv):
    standard = date(1,1,1)
    df = pd.read_csv(query_csv)
    q1 = pd.to_datetime(df['date'])
    json_open = open('1000_testdata_metadata/mt.json', 'r')
    json_load = json.load(json_open)
    result = {}

    max_date = (q1.max().to_pydatetime().date() - standard).days
    min_date = (q1.min().to_pydatetime().date() - standard).days
    query_count = len(q1)

    for k, v in json_load.items():
        if v['start'] <= max_date and min_date <= v['end']:
            count_density = v['count'] / query_count
            if count_density > 1:
                count_density = 1
            app_joinability = (min(v['end'], max_date) - max(v['start'], min_date)) / (max_date - min_date) * count_density
            result[k] = app_joinability

    sorted_result = sorted(result.items(), key=lambda x:x[1], reverse=True)
    return sorted_result[:30]


def NPTJ5(query_csv):
    standard = date(1,1,1)
    df = pd.read_csv(query_csv)
    q1 = pd.to_datetime(df['date'])
    result = {}

    max_date = (q1.max().to_pydatetime().date() - standard).days
    min_date = (q1.min().to_pydatetime().date() - standard).days
    th = (max_date - min_date) // 5
    query_hist_5 = [0 for i in range(5)]
    for i in range(5):
        hist_min_date = min_date + (i * th)
        hist_max_date = min_date + ((i+1) * th)
        if i == 4:
            hist_max_date = max_date

        num = 0
        for x in q1:
            reco = (x.to_pydatetime().date() - standard).days
            if reco >= hist_min_date and reco < hist_max_date:
                num += 1
            elif reco > hist_max_date:
                break
        
        query_hist_5[i] = cl.OrderedDict({"min": hist_min_date, "max": hist_max_date, "num": num})

    for filename in glob.glob(os.path.join('./1000_testdata_5metadata/', '*.json')):
        json_open = open(filename, 'r')
        json_load = json.load(json_open)
        splitname = os.path.basename(filename).split('.', 1)[0]
        candidate_hist_5 = json_load[splitname]['hist_values']
        density_satisfaction = 0
        range_satisfaction = (min(query_hist_5[4]['max'], candidate_hist_5[4]['max']) - max(query_hist_5[0]['min'], candidate_hist_5[0]['min'])) / (query_hist_5[4]['max'] - query_hist_5[0]['min'])

        for i in range(5):
            query_hist_density = query_hist_5[i]['num'] / (query_hist_5[i]['max'] - query_hist_5[i]['min'])
            for j in range(5):
                if candidate_hist_5[j]['min'] <= query_hist_5[i]['min'] < candidate_hist_5[j]['max']:
                    query_hist_start = j
                if candidate_hist_5[j]['min'] <= query_hist_5[i]['max'] < candidate_hist_5[j]['max']:
                    query_hist_goal = j
            
            #query_hist_start == query_hist_goal:
            candidate_hist_density = candidate_hist_5[i]['num'] / (candidate_hist_5[i]['max'] - candidate_hist_5[i]['min'])
            this_hist_density = candidate_hist_density / query_hist_density
            if this_hist_density > 1:
                this_hist_density = 1
            
            density_satisfaction += this_hist_density / 5

        joinability = range_satisfaction * density_satisfaction
        result[splitname] = joinability
        
    sorted_result = sorted(result.items(), key=lambda x:x[1], reverse=True)
    return sorted_result[:30]


def NPTJ20(query_csv):
    standard = date(1,1,1)
    df = pd.read_csv(query_csv)
    q1 = pd.to_datetime(df['date'])
    result = {}

    max_date = (q1.max().to_pydatetime().date() - standard).days
    min_date = (q1.min().to_pydatetime().date() - standard).days
    th = (max_date - min_date) // 20
    query_hist_20 = [0 for i in range(20)]
    for i in range(20):
        hist_min_date = min_date + (i * th)
        hist_max_date = min_date + ((i+1) * th)
        if i == 19:
            hist_max_date = max_date

        num = 0
        for x in q1:
            reco = (x.to_pydatetime().date() - standard).days
            if reco >= hist_min_date and reco < hist_max_date:
                num += 1
            elif reco > hist_max_date:
                break
            
        query_hist_20[i] = cl.OrderedDict({"min": hist_min_date, "max": hist_max_date, "num": num})

    for filename in glob.glob(os.path.join('./1000_testdata_20metadata/', '*.json')):
        json_open = open(filename, 'r')
        json_load = json.load(json_open)
        splitname = os.path.basename(filename).split('.', 1)[0]
        candidate_hist_20 = json_load[splitname]['hist_values']
        density_satisfaction = 0
        range_satisfaction = (min(query_hist_20[19]['max'], candidate_hist_20[19]['max']) - max(query_hist_20[0]['min'], candidate_hist_20[0]['min'])) / (query_hist_20[19]['max'] - query_hist_20[0]['min'])

        for i in range(20):
            query_hist_density = query_hist_20[i]['num'] / (query_hist_20[i]['max'] - query_hist_20[i]['min'])
            for j in range(20):
                if candidate_hist_20[j]['min'] <= query_hist_20[i]['min'] < candidate_hist_20[j]['max']:
                    query_hist_start = j
                if candidate_hist_20[j]['min'] <= query_hist_20[i]['max'] < candidate_hist_20[j]['max']:
                    query_hist_goal = j
            
            #query_hist_start == query_hist_goal:
            candidate_hist_density = candidate_hist_20[i]['num'] / (candidate_hist_20[i]['max'] - candidate_hist_20[i]['min'])
            this_hist_density = candidate_hist_density / query_hist_density
            if this_hist_density > 1:
                this_hist_density = 1
            
            density_satisfaction += this_hist_density / 20

        joinability = range_satisfaction * density_satisfaction
        result[splitname] = joinability
        
    sorted_result = sorted(result.items(), key=lambda x:x[1], reverse=True)
    return sorted_result[:30]


def NPTJ100(query_csv):
    standard = date(1,1,1)
    df = pd.read_csv(query_csv)
    q1 = pd.to_datetime(df['date'])
    result = {}

    max_date = (q1.max().to_pydatetime().date() - standard).days
    min_date = (q1.min().to_pydatetime().date() - standard).days
    th = (max_date - min_date) // 100
    th_x10 = (max_date - min_date) // 10
    query_hist_100 = [0 for i in range(100)]
    for i in range(100):
        hist_min_date = min_date + (i * th)
        hist_max_date = min_date + ((i+1) * th)
        if (i+1) % 10 == 0:
            hist_max_date = min_date + (((i+1)//10) * th_x10)
        if i == 99:
            hist_max_date = max_date

        num = 0
        for x in q1:
            reco = (x.to_pydatetime().date() - standard).days
            if reco >= hist_min_date and reco < hist_max_date:
                num += 1
            elif reco > hist_max_date:
                break
            
        query_hist_100[i] = cl.OrderedDict({"min": hist_min_date, "max": hist_max_date, "num": num})

    for filename in glob.glob(os.path.join('./1000_testdata_100metadata/', '*.json')):
        json_open = open(filename, 'r')
        json_load = json.load(json_open)
        splitname = os.path.basename(filename).split('.', 1)[0]
        candidate_hist_100 = json_load[splitname]['hist_values']
        density_satisfaction = 0
        range_satisfaction = (min(query_hist_100[99]['max'], candidate_hist_100[99]['max']) - max(query_hist_100[0]['min'], candidate_hist_100[0]['min'])) / (query_hist_100[99]['max'] - query_hist_100[0]['min'])

        for i in range(100):
            query_hist_density = query_hist_100[i]['num'] / (query_hist_100[i]['max'] - query_hist_100[i]['min'])
            for j in range(100):
                if candidate_hist_100[j]['min'] <= query_hist_100[i]['min'] < candidate_hist_100[j]['max']:
                    query_hist_start = j
                if candidate_hist_100[j]['min'] <= query_hist_100[i]['max'] < candidate_hist_100[j]['max']:
                    query_hist_goal = j
                if query_hist_100[i]['max'] < candidate_hist_100[j]['min']:
                    break
            
            #query_hist_start == query_hist_goal:
            candidate_hist_density = candidate_hist_100[i]['num'] / (candidate_hist_100[i]['max'] - candidate_hist_100[i]['min'])
            this_hist_density = candidate_hist_density / query_hist_density
            if this_hist_density > 1:
                this_hist_density = 1
            
            density_satisfaction += this_hist_density / 100

        joinability = range_satisfaction * density_satisfaction
        result[splitname] = joinability
        
    sorted_result = sorted(result.items(), key=lambda x:x[1], reverse=True)
    return sorted_result[:30]