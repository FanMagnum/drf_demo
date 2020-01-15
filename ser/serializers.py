#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    : serializers.py
@Time    : 2020/1/9 14:09
@Author  : Lone
@Email   : fanml@neusoft.com
"""
from rest_framework import serializers

# 3. 自定义函数，在序列化器外部，提前声明一个验证代码，然后在声明小圆括号中，通过"validators=[验证函数1，验证函数2...]"
from students.models import Students


def check_name(data):
    if data == '路飞':
        raise serializers.ValidationError('你以为你是海贼王吗，凑不要脸！')
    return data


#  所有的自定义序列化器必须直接或间接继承于 serializers.Serializer
class StudentSerializer(serializers.Serializer):
    # 1.字段声明 要转换的字段 如果写了第二部分代码，有时候也可以不写字段声明
    # 2.可选 如果序列化器继承的是ModelSerializer，则需要声明对应的模型和字段，ModelSerializer是Serializer的子类
    # 3.可选 用于对客户端提供的数据进行验证
    # 4.可选 用于把通过验证的数据进行数据库操作，保存到数据库
    id = serializers.IntegerField()
    name = serializers.CharField()
    age = serializers.IntegerField()
    sex = serializers.BooleanField()
    class_null = serializers.CharField()
    description = serializers.CharField()


"""
在drf中，对于客户端提供的数据，往往需要验证数据的有效性，这部分代码是写在序列化器中的
在序列化器中，已经提供三个地方给我们针对客户提交的数据进行验证
1. 内置选项，字段声明的小括号中，以选项存在作为验证提交
2. 自定义方法，在序列化器中作为对象方法来提供验证 这部分验证的方法，必须以"validate_<字段>"或者"validate"作为方法名
3. 自定义函数，在序列化器外部，提前声明一个验证代码，然后在声明小圆括号中，通过"validators=[验证函数1，验证函数2...]"
"""


class StudentVSerializer(serializers.Serializer):
    # 1. 内置选项，字段声明的小括号中，以选项存在作为验证提交
    name = serializers.CharField(max_length=20, min_length=2, validators=[check_name])
    age = serializers.IntegerField(max_value=50, min_value=1)
    sex = serializers.BooleanField(required=True)
    class_null = serializers.CharField(max_length=20, min_length=2)
    # 2. 自定义方法，在序列化器中作为对象方法来提供验证 这部分验证的方法，必须以"validate_<字段>"或者"validate"作为方法名
    """验证单个字段的数据"""

    def validate_name(self, data):
        if data == 'root':
            raise serializers.ValidationError('用户名不能为root')
        # 验证方法中结束时必须返回本次验证内容
        return data

    """验证多个字段的数据"""

    def validate(self, attrs):  # 表示客户端提交的所有数据
        print(f'需要验证的字典：{attrs}')
        name = attrs.get('name')
        if name == '老男孩':
            raise serializers.ValidationError('不能用这个名字您嘞')
        return attrs

    """
    在完成数据验证之后，drf提供了request和response来接收和返回数据
    1. create
    2. update
    """

    def create(self, validate):
        """接收客户提交的新增数据"""
        name = validate.get('name')
        age = validate.get('age')
        sex = validate.get('sex')
        class_null = validate.get('class_null')
        instance = Students.objects.create(
            name=name,
            age=age,
            sex=sex,
            class_null=class_null
        )
        return instance

    def update(self, instance, validated_data):
        """用于在反序列化中更新的数据"""
        name = validated_data.get('name')
        age = validated_data.get('age')
        sex = validated_data.get('sex')
        class_null = validated_data.get('class_null')

        instance.name = name
        instance.age = age
        instance.sex = sex
        instance.class_null = class_null

        instance.save()

        return instance


"""
开发中往往一个资源的序列化和反序列化阶段都是写在一个序列化器中的
"""


class StudentsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=5, min_length=2, validators=[check_name])
    age = serializers.IntegerField(max_value=24, min_value=10)
    sex = serializers.BooleanField(required=True)
    class_null = serializers.CharField(required=True)
    description = serializers.CharField(read_only=True)
    """验证单个字段的数据"""

    def validate_name(self, data):
        if data == 'root':
            raise serializers.ValidationError('用户名不能为root')
        # 验证方法中结束时必须返回本次验证内容
        return data

    """验证多个字段的数据"""

    def validate(self, attrs):  # 表示客户端提交的所有数据
        print(f'需要验证的字典：{attrs}')
        name = attrs.get('name')
        if name == '老男孩':
            raise serializers.ValidationError('不能用这个名字您嘞')
        return attrs

    def create(self, validate):
        """接收客户提交的新增数据"""
        name = validate.get('name')
        age = validate.get('age')
        sex = validate.get('sex')
        class_null = validate.get('class_null')
        instance = Students.objects.create(
            name=name,
            age=age,
            sex=sex,
            class_null=class_null
        )
        return instance

    def update(self, instance, validated_data):
        """用于在反序列化中更新的数据"""
        name = validated_data.get('name')
        age = validated_data.get('age')
        sex = validated_data.get('sex')
        class_null = validated_data.get('class_null')
        instance.name = name
        instance.age = age
        instance.sex = sex
        instance.class_null = class_null
        instance.save()
        return instance


"""
我们可以使用ModelSerializer来完成模型类序列化器的声明
这种基于ModelSerializer声明序列化器的方式有三个优势：
1. 可以直接通过声明当前序列化器从指定的模型中把字段声明引用过来
2. ModelSerializer继承了Serializer的所有功能和方法，同时还编写了create和update
3. 模型中同一个字段中关于验证的选项，也会被引用到序列化器中一并作为选项参与验证
"""
class StudentsModelSerializer(serializers.ModelSerializer):
    # 字段声明  [如果模型中没有的字段，还需要用户提交，则需要手动在这里声明]
    # 指定引用的模型
    class Meta:
        model = Students
        fields = "__all__"

    def validate(self, attrs):
        name = attrs.get('name')
        age = attrs.get('age')
        if name in ['root', '路飞', '小心肝']:
            raise serializers.ValidationError('invalid name')
        if age <= 5:
            raise serializers.ValidationError('You are too young')
        return attrs