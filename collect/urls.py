#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    : urls.py
@Time    : 2020/1/13 10:59
@Author  : Lone
@Email   : fanml@neusoft.com
"""
from django.urls import path
from rest_framework.routers import DefaultRouter

from collect import views

urlpatterns = [
    # 不要在同一个路由的as_view中书写两个相同键值的http方法，会产生覆盖
    path('students/', views.StudentViewSet.as_view({'get': "get_10"})),
    path('students/get5girl', views.StudentViewSet.as_view({'get': "get_5_girl"})),
    path('students/<int:pk>', views.StudentViewSet.as_view({'get': "get_one"})),
    path('students1/', views.StudentsGenericViewSet.as_view({'get': "get_10"})),
    path('students1/get5girl', views.StudentsGenericViewSet.as_view({'get': "get_5_girl"})),
    path('students1/<int:pk>', views.StudentsGenericViewSet.as_view({'get': "get_one"})),
    path('students2/', views.StudentsMixinViewSet.as_view({'get': "list", 'post': 'create'})),
    path('students2/<int:pk>', views.StudentsMixinViewSet.as_view({'get': "retrieve", 'put': 'update', 'delete': 'destroy'})),
    path('students3/', views.StudentsModelViewSet.as_view({'get': "list", 'post': 'create'})),
    path('students3/<int:pk>', views.StudentsModelViewSet.as_view({'get': "retrieve", 'put': 'update', 'delete': 'destroy'})),
    path('students4/', views.StudentsReadOnlyModelViewSet.as_view({'get': 'list'})),
    path('students4/<int:pk>', views.StudentsReadOnlyModelViewSet.as_view({'get': 'retrieve'})),
    # 一个视图类中调用多个序列化器
    path('students6/', views.StudentTwoSerializerAPIView.as_view()),
    # 一个视图集中调用多个序列化器
    #path('students7/', views.StudentTwoSerializerModelViewSet.as_view())
]

"""
有了视图集以后，视图文件中多个视图类可以合并成一个，但是路由的代码就变得复杂
需要我们经常在as_view方法编写http请求和视图方法的对应关系
事实上，在路由中，DRF也提供了一个路由类给我们对路由的代码进行简写
当然，这个路由类仅针对视图集才可以使用
"""

# 路由实例化
# 路由类默认只会给视图集中的基本API生成地址 [list create retrieve update destroy]
# 自定义API需要使用@action装饰器
router = DefaultRouter()
# router.register('访问地址前缀', '视图集类', '访问别名')
router.register('students5', views.RouterModelViewSet)
router.register('students7', views.StudentTwoSerializerModelViewSet)
urlpatterns += router.urls
