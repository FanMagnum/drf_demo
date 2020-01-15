#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    : urls.py
@Time    : 2020/1/10 15:29
@Author  : Lone
@Email   : fanml@neusoft.com
"""
from django.urls import path

from req import views

urlpatterns = [
    path('student/', views.StudentView.as_view()),
    path('student1/', views.StudentAPIView.as_view()),
    path('students/', views.StudentsAPIView.as_view()),
    path('students1/', views.StudentsGenericAPIView.as_view()),
    path('student/<int:pk>', views.StudentGenericAPIView.as_view()),
    path('students2/', views.StudentsMixinGenericAPIView.as_view()),
    path('student2/<int:pk>', views.StudentMixinGenericAPIView.as_view()),
    path('students3/', views.StudentsListCreateAPIView.as_view()),
    path('student3/<int:pk>', views.StudentRetrieveUpdateDestroyAPIView.as_view()),
    path('students4/', views.StudentsModelViewSet.as_view({'get': "list", 'post': 'create'})),
    path('student4/<int:pk>', views.StudentsModelViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]