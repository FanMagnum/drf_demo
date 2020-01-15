from django.shortcuts import render
# Create your views here.
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Students
from .serializers import StudentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class StandardPageNumberPagination(PageNumberPagination):
    """分页相关配置"""
    # 分页参数page
    page_query_param = 'page'
    # 默认每页5条数据
    page_size = 5
    # 用户可以根据size参数自定义每页数据数量
    page_size_query_param = 'size'
    # 最大页数
    max_page_size = None


class StudentAPIView(ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('age', 'name', 'class_null')
    ordering_fields = ('id', 'age', 'class_null')
    pagination_class = StandardPageNumberPagination

    @action(methods=('GET',), detail=False)
    def get_5_girls(self, request):
        girls = self.get_queryset().filter(sex=False).order_by('age')[:5]
        serializer = self.get_serializer(instance=girls, many=True)
        return Response(serializer.data)
