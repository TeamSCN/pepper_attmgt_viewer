from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import os

from .models import Attendance
from .models import ImageFile


def index(request):
    latest_att_list = Attendance.objects.order_by('-date')
    context = {'latest_question_list': latest_att_list}
    return render(request, 'attmgt/index.html', context)

@require_POST
@csrf_exempt
def receive_image(request):
    image = request.FILES["image"]
    x, y = image.name.split('_')[1].split('-')
    y = y.rsplit('.', 1)[0]
    image = ImageFile(x=float(x), y=float(y), image=image)
    image.save()
    # print(request)
    return HttpResponse()
