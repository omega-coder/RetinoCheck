# -*- encoding: utf-8 -*-


from django.db import models
from datetime import datetime


def f(instance, filename):
    ext = filename.split(".")[-1]
    if instance.pk:
        return "{}/{}.{}".format(datetime.now().strftime("%Y"), instance.pk, ext)
    else:
        pass


class TestImage(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, primary_key=True)
    image = models.ImageField(upload_to=f)
    author = models.CharField(max_length=255, null=True, default="admin")
    pred_class = models.CharField(max_length=10)
    preds = models.CharField(max_length=255, null=True)
    uploaded_at = models.DateTimeField(default=datetime.now)
    real_label = models.CharField(max_length=10, null=True, blank=True, default="")
