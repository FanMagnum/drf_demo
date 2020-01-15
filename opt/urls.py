#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    : urls.py
@Time    : 2020/1/13 16:30
@Author  : Lone
@Email   : fanml@neusoft.com
"""
from django.urls import path

from opt import views

urlpatterns = [
    path('auth/', views.DemoAPIView.as_view()),
    path('auth2/', views.Demo2APIView.as_view()),
    path('vote/', views.Demo4APIView.as_view()),
    path('students/', views.Demo5APIView.as_view()),
    path('order/', views.Demo6APIView.as_view()),
    path('page/', views.Demo7APIView.as_view()),
    path('error/', views.Demo8APIView.as_view()),
]