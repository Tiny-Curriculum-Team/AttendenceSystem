from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, date
from calendar import monthrange

from WriteIn.models import Number

from django.db.models import Avg

from django.db.models import Max,Min

import yaml

GLOBAL_DATA = yaml.load(open('../config.yml'), Loader=yaml.FullLoader)
# Create your views here.
def compute(request):
    if request.method == "GET":
        today = datetime.today()
        last_day = monthrange(today.year, today.month)
        start_time = request.GET['start_time'] or date(today.year, today.month, day=1)
        terminal_time = request.GET['terminal_time'] or date(today.year, today.month, day=last_day)
        timezone = [start_time, terminal_time]
        query_data = query(timezone)  # multi-dimensions array obj
        on_time_rate = arrive_on_time_rate(query_data)
        be_late_rate = arrive_late_rate(query_data)
        leaving_early_rate = leave_early_rate(query_data)
        amount_range = total_amount_in_time_range(query_data)

        return JsonResponse({
            "on_time": on_time_rate,
            "be_late": be_late_rate,
            "leaving_early": leaving_early_rate,
            "count": amount_range
        })
    else:
        return render("请求方法错误！")


def query(time_range: list):
    date_query=Number.objects.filter(date_time__gt=time_range[0],data_time__lt=time_range[1])
    return date_query


#道勤人数
def arrive_on_time_rate(data):
    date_arrive_on_time_rate=data.objects.all().aggregate(Max('count'))
    return int(date_arrive_on_time_rate.count)


#道勤率
def arrive_on_time_rate(data):
    date_arrive_on_time_rate=data.objects.all().aggregate(Max('count'))
    return date_arrive_on_time_rate.count * 1.0 / GLOBAL_DATA['TOTAL_AMOUNT']


#迟到率
def arrive_late_rate(data):
    min_count = data.objects.all().aggregate(Min('count'))
    data=GLOBAL_DATA-min_count
    return data


# 早退人数
def leave_early_rate(data):
    min_count = data.objects.all().aggregate(Min('count'))
    max_count = data.objects.all().aggregate(Max('count'))
    data_leave_early_rate = max_count - min_count
    return int(data_leave_early_rate)


# 早退率
def leave_early_rate(data):
    min_count = data.objects.all().aggregate(Min('count'))
    max_count = data.objects.all().aggregate(Max('count'))
    data_leave_early_rate = max_count - min_count
    return data_leave_early_rate * 1.0 / GLOBAL_DATA['TOTAL_AMOUNT']


# 平均人数
def total_amount_in_time_range(data):
    avg=data.objects.all().aggregate(Avg('count'))
    return float(avg)
