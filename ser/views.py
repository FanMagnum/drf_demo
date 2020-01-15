from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from ser.serializers import StudentSerializer, StudentVSerializer, StudentsSerializer, StudentsModelSerializer
from students.models import Students

import json

class StudentNameView(View):
    def get(self, request, name):
        student = Students.objects.get(name=name)
        serializer = StudentSerializer(student)
        print(serializer.data)
        return HttpResponse("OK")


class StudentIdView(View):
    def get(self, request, pk):
        print(pk, type(pk))
        student = Students.objects.get(pk=pk)
        serializer = StudentSerializer(student)
        print(serializer.data)
        return HttpResponse('OK')


class StudentsView(View):
    def get(self, request):
        """获取所有数据"""
        students = Students.objects.all()
        # 序列化器转换多个数据
        # 必须声明many=True
        serializer = StudentsSerializer(students, many=True)
        # 返回多个数据 safe=False
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        """添加数据"""
        data_string = request.body.decode()
        data_dict = json.loads(data_string)
        # 调用序列化器
        serializer = StudentsSerializer(data=data_dict)
        # 执行验证
        serializer.is_valid(raise_exception=True)
        # 执行数据反序列化
        instance = serializer.save()
        return JsonResponse(serializer.data)


class CreateStudentView(View):
    def post(self, request):
        date_string = request.body.decode()
        data_dict = json.loads(date_string)
        print(data_dict)

        serializer = StudentVSerializer(data=data_dict)
        # 调用序列化器进行实例化
        # is_valid在执行的时候，会自动先后调用，字段的内置选项
        # 调用序列化器中写好额验证代码
        # raise_exception=True 跑出验证错误信息，并阻止代码继续往后运行
        result = serializer.is_valid(raise_exception=True)
        print(f"验证结果：{result}")
        print(f"{serializer.error_messages}")
        # 获取被验证后的数据
        print(f'验证后的数据：{serializer.validated_data}')
        # save表示让序列化器开始执行反序列化代码 create和update的代码
        student = serializer.save()
        print(f'更新数据库成功 {student}')
        return HttpResponse('OK')


class UpdateStudentView(View):
    def put(self, request, pk):
        """在更新中调用序列化器完成数据更新"""
        instance = Students.objects.get(pk=pk)
        data_string = request.body.decode()
        data_dict = json.loads(data_string)
        serializer = StudentVSerializer(instance=instance, data=data_dict)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        print(instance)
        return HttpResponse('Update Successful')

"""
ModelSerializer使用
"""
class StudentsModelView(View):
    def get(self, request):
        """获取所有数据"""
        students = Students.objects.all()
        # 序列化器转换多个数据
        # 必须声明many=True
        serializer = StudentsModelSerializer(instance=students, many=True)
        # 返回多个数据 safe=False
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        """添加数据"""
        data_string = request.body.decode()
        data_dict = json.loads(data_string)
        # 调用序列化器
        serializer = StudentsModelSerializer(data=data_dict)
        # 执行验证
        serializer.is_valid(raise_exception=True)
        # 执行数据反序列化
        instance = serializer.save()
        return JsonResponse(serializer.data)