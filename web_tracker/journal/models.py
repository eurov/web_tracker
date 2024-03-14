from django.db import models


class Visit(models.Model):
    domain = models.CharField(max_length=150)
    link = models.CharField(max_length=250)
    time = models.DateTimeField(auto_now_add=True)
