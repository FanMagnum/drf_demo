#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    : serializers.py
@Time    : 2020/1/9 14:54
@Author  : Lone
@Email   : fanml@neusoft.com
"""
from rest_framework import serializers

from students.models import Students


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'