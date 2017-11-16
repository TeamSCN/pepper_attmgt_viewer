from django.contrib import admin

from .models import Attendance
from .models import ImageFile

admin.site.register(Attendance)
admin.site.register(ImageFile)
