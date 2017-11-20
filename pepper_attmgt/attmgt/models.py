from django.db import models
import datetime


class Attendance(models.Model):
    # date = models.DateTimeField('date')
    student_id = models.PositiveIntegerField(default=0)
    date = models.DateField(default=datetime.date.today())
    time = models.TimeField(default=datetime.datetime.now().time())
    att = models.BooleanField()
    # att = models.PositiveIntegerField(default=0)

    # def __str__(self):
    #     return self.date.strftime('%Y-%m-%d %H:%M:%S')

class ImageFile(models.Model):
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='images')
