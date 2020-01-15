#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    : exceptions.py
@Time    : 2020/1/14 10:03
@Author  : Lone
@Email   : fanml@neusoft.com
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    :param exc:    发生异常时的异常对象
    :param context: 发生异常时的执行上下文
    :return:
    """
    response = exception_handler(exc, context)
    if not response:
        if isinstance(exc, ZeroDivisionError):
            print('0不能作为除数')
            return Response('服务器内部错误！', status=status.HTTP_500_INTERNAL_SERVER_ERROR)