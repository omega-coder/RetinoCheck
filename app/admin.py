# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import TestImage

class TestImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(TestImage)