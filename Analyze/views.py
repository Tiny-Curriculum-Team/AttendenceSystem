from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, date
from calendar import monthrange


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
    return time_range


def arrive_on_time_rate(data):
    return data


def arrive_late_rate(data):
    return data


def leave_early_rate(data):
    return data


def total_amount_in_time_range(data):
    return data
