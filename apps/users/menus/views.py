'''
-*- coding: utf-8 -*-
@Author  : lingdeng
@Time    : 2020/8/25 10:34 下午
@Software: PyCharm
@File    : serializers.py
@IDE    : PyCharm
'''
# @Time    : 2019/1/12 21:02
# @Author  : xufqing
from rest_framework import viewsets, authentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from common.custom import CommonPagination, RbacPermission, TreeAPIView
from users.menus.serializers import MenuSerializer
from users.models import Menu


class MenuViewSet(ModelViewSet, TreeAPIView):
    '''
    菜单管理：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'menu_all'}, {'get': 'menu_list'}, {'post': 'menu_create'}, {'put': 'menu_edit'},
                 {'delete': 'menu_delete'})
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    pagination_class = CommonPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('sort',)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (RbacPermission,)


class MenuTreeView(TreeAPIView, viewsets.GenericViewSet):
    '''
    菜单树
    '''
    queryset = Menu.objects.all()
