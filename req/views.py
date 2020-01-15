from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from req.serializers import StudentsModelSerializer
from students.models import Students


class StudentView(View):
    def get(self, request):
        data = {'name': '小花', 'age': 10}
        return JsonResponse(data)


class StudentAPIView(APIView):
    def get(self, request):
        data = {'name': '小花', 'age': 10}
        return Response(data)


"""
使用APIView提供学生信息的5个API接口
GET    /req/students/     获取全部数据
POST   /req/students/     添加数据
GET    /req/students/<int:id>   获取一条数据
PUT    /req/students/<int:id>   更新一条数据
DELETE /req/students/<int:id>  删除一天数据
"""


class StudentsAPIView(APIView):
    def get(self, request):
        """获取全部数据"""
        students = Students.objects.all()
        serializer = StudentsModelSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        """添加数据"""
        serializer = StudentsModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


"""
使用APIView提供学生信息的5个API接口
GET    /req/students/     获取全部数据
POST   /req/students/     添加数据
GET    /req/students/<int:id>   获取一条数据
PUT    /req/students/<int:id>   更新一条数据
DELETE /req/students/<int:id>  删除一天数据
"""


class StudentsGenericAPIView(GenericAPIView):
    # 当前视图类中操作的公共数据，先从数据库查询出来
    queryset = Students.objects.all()
    # 设置类视图中所有方法共有调用的视图类
    serializer_class = StudentsModelSerializer

    def get(self, request):
        """获取所有数据"""
        students = self.get_queryset()
        serializer = self.get_serializer(instance=students, many=True)
        return Response(serializer.data)

    def post(self, request):
        """添加数据"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class StudentGenericAPIView(GenericAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentsModelSerializer

    def get(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data)

    def put(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        instance = self.get_object()
        instance.delete()
        return Response('')


"""
使用GenericAPIView结合视图Mixin扩展类，快速实现数据接口的API View
ListModelMixin:     实现查询所有数据功能
CreateModelMixin：   实现添加数据的功能
RetrieveModelMixin: 实现查询一条数据功能 
UpdateModelMixin:   更新一条数据的功能
DestroyModelMixin:  删除一条数据的功能
"""


class StudentsMixinGenericAPIView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Students.objects.all()
    serializer_class = StudentsModelSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class StudentMixinGenericAPIView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Students.objects.all()
    serializer_class = StudentsModelSerializer

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.destroy(request)


"""
DRF下面，内置了一些同时继承了GenericAPIView和Mixin扩展类的视图子类，我们可以直接继承这些子类就可以生成对应的API接口
ListAPIView 获取所有数据
CreateAPIView 添加数据
ListCreateAPIView
RetrieveAPIView 获取一条数据
UpdateAPIView 更新一条数据
DestroyAPIView 删除一条数据
RetrieveUpdateDestroyAPIView
"""


# 获取所有数据
class StudentsListCreateAPIView(ListCreateAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentsModelSerializer


class StudentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentsModelSerializer


"""
视图集
上面5个接口使用8行代码生成，但是有一半的代码重复
所以，我们要把这些重复的代码进行整合，但是依靠原来的类视图，其实是有2方面产生冲突的
1.查询所有数据、添加数据是不需要声明pk的，而其他接口需要 [路由冲突]
2.查询所有数据和查询一条数据，都是get请求 [请求方法冲突]
为了解决以上问题，DRF提供了视图集解决
"""


class StudentsModelViewSet(ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsModelSerializer
