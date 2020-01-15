#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    : urls.py
@Time    : 2020/1/9 14:48
@Author  : Lone
@Email   : fanml@neusoft.com
"""

urlpatterns = []

from rest_framework.routers import DefaultRouter
from students import views

router = DefaultRouter()
router.register('', views.StudentAPIView)
urlpatterns += router.urls
