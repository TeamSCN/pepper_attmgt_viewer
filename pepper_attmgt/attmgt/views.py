from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Case, When
import os
import datetime

from .models import Attendance


def index(request):
    #latest_att_list = Attendance.objects.order_by('-date')
    latest_date = Attendance.objects.latest('date').date
    today_date = datetime.datetime.today()
    yest_date = datetime.datetime.today() - datetime.timedelta(1)
    today_num_att = Attendance.objects.filter(date=today_date).aggregate(att=Count(Case(When(att=True, then=1))))
    yest_num_att = Attendance.objects.filter(date=yest_date).aggregate(att=Count(Case(When(att=True, then=1))))

    l1_7_date = []
    for i in range(1, 8):
        l1_7_date.append(datetime.datetime.today() - datetime.timedelta(i))
    l1_7_num_att = []
    for i in range(len(l1_7_date)):
        l1_7_num_att.append(Attendance.objects.filter(date=l1_7_date[i]).aggregate(att=Count(Case(When(att=True, then=1)))))
        l1_7_date[i] = l1_7_date[i].strftime("%m.%d")

    context = {'today': {'today_date': today_date.strftime("%Y/%m/%d"), 'today_num_att': today_num_att},
               'yest': {'yest_date': yest_date.strftime("%Y/%m/%d"), 'yest_num_att': yest_num_att},
               'l1_7': {'l1_7_date': l1_7_date, 'l1_7_num_att': l1_7_num_att}}
    return render(request, 'attmgt/index.html', context)
