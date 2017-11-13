from django.db import models
import datetime


class Attendance(models.Model):
    # date = models.DateTimeField('date')
    student_id = models.PositiveIntegerField(default=0)
    date = models.DateField()
    time = models.TimeField(default=datetime.time(0, 0, 0))
    att = models.BooleanField()
    # att = models.PositiveIntegerField(default=0)

    # def __str__(self):
    #     return self.date.strftime('%Y-%m-%d %H:%M:%S')
