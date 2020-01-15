#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    : urls.py
@Time    : 2020/1/9 14:37
@Author  : Lone
@Email   : fanml@neusoft.com
"""
from django.urls import path

from ser import views

urlpatterns = [
    path('student/<str:name>/', views.StudentNameView.as_view()),
    path('student/id/<int:pk>/', views.StudentIdView.as_view()),
    path('students/', views.StudentsView.as_view()),
    # 对提交数据进行验证
    path('student/', views.CreateStudentView.as_view()),
    # 反序列化
    path('student2/<int:pk>/', views.UpdateStudentView.as_view()),
    path('student3/', views.StudentsModelView.as_view()),
]