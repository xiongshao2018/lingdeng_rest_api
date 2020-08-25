'''
-*- coding: utf-8 -*-
@Author  : lingdeng
@Time    : 2020/8/25 10:34 下午
@Software: PyCharm
@File    : serializers.py
@IDE    : PyCharm
'''
from rest_framework import serializers

from users.models import Menu


class MenuSerializer(serializers.ModelSerializer):
    '''
    菜单序列化
    '''

    class Meta:
        model = Menu
        fields = ('id', 'name', 'icon', 'path', 'is_show', 'is_frame', 'sort', 'component', 'pid')
        extra_kwargs = {'name': {'required': True, 'error_messages': {'required': '必须填写菜单名'}}}
