from django.db import models


class Attendance(models.Model):
    date = models.DateTimeField('date')
    att = models.IntegerField(default=0)

    def __str__(self):
        return self.date.strftime('%Y-%m-%d %H:%M:%S')
