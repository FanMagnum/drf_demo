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