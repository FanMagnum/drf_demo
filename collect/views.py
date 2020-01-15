from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

from collect.serializers import StudentsModelSerializer, StudentInfoModelSerializer
from students.models import Students

"""
视图集
ViewSet继承于APIView
"""


class StudentViewSet(ViewSet):

    def get_10(self, request):
        student_list = Students.objects.all()[:10]
        serializer = StudentsModelSerializer(instance=student_list, many=True)
        return Response(serializer.data)

    def get_one(self, request, pk):
        student = Students.objects.get(pk=pk)
        serializer = StudentsModelSerializer(instance=student)
        return Response(serializer.data)

    def get_5_girl(self, request):
        girls = Students.objects.filter(sex=False)[:5]
        serializer = StudentsModelSerializer(instance=girls, many=True)
        return Response(serializer.data)


"""
如果希望在视图集中调用GenericAPIView的功能，则可以采用以下方式
"""


class StudentsGenericViewSet(GenericViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsModelSerializer

    def get_10(self, request):
        instance = self.get_queryset()[:10]
        serializer = self.get_serializer(instance=instance, many=True)
        return Response(serializer.data)

    def get_one(self, request, pk):
        instance = self.get_object()
        serializer = StudentsModelSerializer(instance=instance)
        return Response(serializer.data)

    def get_5_girl(self, request):
        instance = self.get_queryset().filter(sex=False)[:5]
        serializer = StudentsModelSerializer(instance=instance, many=True)
        return Response(serializer.data)


"""
在使用GenericViewSet时，虽然已经提供了基本调用数据集（queryset）和序列化器属性，但我们要编写一些基本的
API时，还是需要调用DRF提供的模型扩展类[Mixins]
"""


class StudentsMixinViewSet(GenericViewSet, ListModelMixin, CreateModelMixin,
                           RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Students.objects.all()
    serializer_class = StudentsModelSerializer


"""
ModelViewSet继承以上五种Mixins所以可以快速生成五个接口
"""


class StudentsModelViewSet(ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsModelSerializer


"""
只读模型视图集
"""


class StudentsReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsModelSerializer


"""
路由的使用
"""


class RouterModelViewSet(ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsModelSerializer

    @action(methods=['GET', 'POST'], detail=False)
    # methods 指定允许哪些http请求访问当前视图方法
    # detail  指定生成的路由地址中是否要夹带pk值
    def get_11(self, request):
        return Response({'age': 11})


"""
在多个视图类合并成一个视图类以后，那么有时候会出现一个类中需要调用多个序列化器
"""
"""
在视图类中调用多个序列化器
原来的视图类中基本上一个视图类只会调用一个序列化器
当然如果要调用多个序列化器
"""


class StudentTwoSerializerAPIView(GenericAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentInfoModelSerializer

    # 在一个视图类中调用多个序列化器
    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return StudentInfoModelSerializer
    #     else:
    #         return StudentsModelSerializer

    def get(self, request):
        students = self.get_queryset()
        serializer = self.get_serializer(instance=students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


"""在视图集中调用多个序列化器"""


class StudentTwoSerializerModelViewSet(ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsModelSerializer
    """
        要求：
            列表数据list，返回两个字段
            详情数据retrieve，返回所有字段
    """
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StudentsModelSerializer
        else:
            return StudentInfoModelSerializer