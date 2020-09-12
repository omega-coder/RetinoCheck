# -*- encoding: utf-8 -*-


from django.urls import path
from app import views

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("results/", views.results, name="results"),
    path("result/<str:name>", views.result_name, name="result_name"),
    path("predict/", views.prediction, name="predict"),
    path("image/labelize/<int:page>/", views.image_labelize, name="labelize"),
    path("prediction/correct", views.correct_prediction, name="correct_pred"),
    path("report/generate/<str:name>/", views.gen_report, name="genreport"),
    path("", views.index, name="home"),
]
