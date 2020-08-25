'''
-*- coding: utf-8 -*-
@Author  : lingdeng
@Time    : 2020/8/25 10:34 下午
@Software: PyCharm
@File    : serializers.py
@IDE    : PyCharm
'''
from rest_framework import serializers

from users.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    '''
    组织架构序列化
    '''
    type = serializers.ChoiceField(choices=Organization.organization_type_choices, default='company')

    class Meta:
        model = Organization
        fields = '__all__'


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField(max_length=20, source='name')


class OrganizationUserTreeSerializer(serializers.ModelSerializer):
    '''
    组织架构树序列化
    '''
    label = serializers.StringRelatedField(source='name')
    children = UserSerializer(many=True, read_only=True, source='userprofile_set')

    class Meta:
        model = Organization
        fields = ('id', 'label', 'pid', 'children')
