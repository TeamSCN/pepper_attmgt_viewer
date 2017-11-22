from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Case, When
import os
import datetime

from .models import Attendance
from .models import ImageFile


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
    l1_7_month = []
    l1_7_day = []
    for i in range(len(l1_7_date)):
        l1_7_num_att.append(Attendance.objects.filter(date=l1_7_date[i]).aggregate(att=Count(Case(When(att=True, then=1)))))
        l1_7_month.append(l1_7_date[i].strftime("%m"))
        l1_7_day.append(l1_7_date[i].strftime("%d"))

    context = {'today': {'today_date': today_date.strftime("%Y/%m/%d"), 'today_num_att': today_num_att},
               'yest': {'yest_date': yest_date.strftime("%Y/%m/%d"), 'yest_num_att': yest_num_att},
               'l1_7': {'l1_7_month': l1_7_month, 'l1_7_day': l1_7_day, 'l1_7_num_att': l1_7_num_att}}
    return render(request, 'attmgt/index.html', context)


def image(request):
    image_list = ImageFile.objects.all().order_by('-id')
    context = {'image_list': image_list}
    return render(request, 'attmgt/detection_image.html', context)
