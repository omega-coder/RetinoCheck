# -*- encoding: utf-8 -*-


from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model


def f(instance, filename):
    ext = filename.split(".")[-1]
    if instance.pk:
        return "{}/{}.{}".format(datetime.now().strftime("%Y"), instance.pk, ext)
    else:
        pass

class DRModel(models.Model):
    name = models.CharField(max_length=40, unique=True, null=False)
    date_added = models.DateTimeField(default=datetime.now)
    model_type = models.PositiveIntegerField()
    author = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

class TestImage(models.Model):
    LEFT = "L"
    RIGHT = "R"
    EYE_ORIENTATION_CHOICES = [
        (LEFT, 'LEFT'),
        (RIGHT, 'RIGHT'),
    ]
    name = models.CharField(max_length=100, unique=True,
                            null=False, primary_key=True)
    image = models.ImageField(upload_to=f)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    pred_class = models.PositiveIntegerField()
    preds = models.CharField(max_length=255, null=True)
    uploaded_at = models.DateTimeField(default=datetime.now)
    real_label = models.PositiveIntegerField(default=None, null=True)
    eye_orientation = models.CharField(
        max_length=1, choices=EYE_ORIENTATION_CHOICES, null=True, default=None)
    model = models.ForeignKey(DRModel, on_delete=models.SET_NULL, null=True)


