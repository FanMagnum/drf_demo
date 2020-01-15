from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission

from opt.serializers import StudentsModelSerializer
from students.models import Students


class DemoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """个人中心"""
        return Response('身份验证')


class Demo2APIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response('管理员')


class MyPermission(BasePermission):
    def has_permission(self, request, view):
        """
        :param request: 本次操作的http请求对象
        :param view:    本次访问路由对应的视图对象
        :return:
        """
        if request.query_params.get('user') == 'fan':
            return True
        else:
            return False


class Demo3APIView(APIView):
    permission_classes = [MyPermission]

    def get(self, request):
        return Response('指定用户')


class Demo4APIView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request):
        """投票页面"""
        return Response('投票页面')


"""过滤"""
class Demo5APIView(ListAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentsModelSerializer
    # 过滤
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('age', 'name')
    # def get(self, request):
    #     students = self.get_queryset()
    #     serializer = self.get_serializer(instance=students, many=True)
    #     return Response(serializer.data)


"""排序"""
class Demo6APIView(ListAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentsModelSerializer
    # 排序
    filter_backends = (OrderingFilter,)
    ordering_fields = ('id', 'age')
    # def get(self, request):
    #     students = self.get_queryset()
    #     serializer = self.get_serializer(instance=students, many=True)
    #     return Response(serializer.data)


"""
分页
1. 自定义分页器，定制分页的相关配置
"""
class StandardPageNumberPagination(PageNumberPagination):
    """分页相关配置"""
    # 分页参数page
    page_query_param = 'page'
    # 默认每页5条数据
    page_size = 5
    # 用户可以根据size参数自定义每页数据数量
    page_size_query_param = 'size'
    # 最大页数
    max_page_size = 10

class Demo7APIView(ListAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentsModelSerializer
    pagination_class = StandardPageNumberPagination

class Demo8APIView(APIView):
    def get(self, request):
        1/0
        return Response('OK')
