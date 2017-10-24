from django.shortcuts import render

from .models import Attendance


def index(request):
    latest_att_list = Attendance.objects.order_by('-date')
    context = {'latest_question_list': latest_att_list}
    return render(request, 'attmgt/index.html', context)
