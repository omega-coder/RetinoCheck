# -*- encoding: utf-8 -*-


from django.urls import path
from app import views

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("results/", views.results, name="results"),
    path("predict/", views.prediction, name="predict"),
    path("image/labelize/", views.image_labelize, name="labelize"),
    path("prediction/correct", views.correct_prediction, name="correct_pred"),
    path("", views.index, name="home"),
]
