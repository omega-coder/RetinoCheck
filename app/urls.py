# -*- encoding: utf-8 -*-


from django.urls import path, re_path
from app import views

urlpatterns = [
    # Matches any html file 
    re_path(r'^.*\.html', views.pages, name='pages'),
    path('profile/', views.profile, name="profile"),
    path('results/', views.results, name='results'),
    path('predict/', views.prediction, name='predict'),
    # The home page
    path('', views.index, name='home'),
]