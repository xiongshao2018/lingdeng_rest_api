'''
-*- coding: utf-8 -*-
@Author  : lingdeng
@Time    : 2020/8/25 10:34 下午
@Software: PyCharm
@File    : serializers.py
@IDE    : PyCharm
'''
from rest_framework import serializers

from users.models import Permission


class PermissionListSerializer(serializers.ModelSerializer):
    '''
    权限列表序列化
    '''
    menuname = serializers.ReadOnlyField(source='menus.name')

    class Meta:
        model = Permission
        fields = ('id', 'name', 'method', 'menuname', 'pid')
