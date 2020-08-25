'''
-*- coding: utf-8 -*-
@Author  : lingdeng
@Time    : 2020/8/25 10:34 下午
@Software: PyCharm
@File    : serializers.py
@IDE    : PyCharm
'''

# @Time    : 2019/1/12 21:03
# @Author  : xufqing

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, authentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from cmdb.models import ConnectionInfo
from common.custom import CommonPagination, RbacPermission
from deployment.models import Project
from lingdeng_rest_api.code import *
from .serializers import ChangePasswdSerializer, ChangePasswdAdminSerializer, UploadAvatarSerializer
from ..models import UserProfile
from ..serializers.user_serializer import UserListSerializer, UserCreateSerializer, UserModifySerializer, \
    UserInfoListSerializer, UserLoginSerializer, UserBuildMenusSerializer


class UserAuthView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    用户认证获取token
    '''
    """登录账号"""
    serializer_class = UserLoginSerializer

    authentication_classes = (authentication.SessionAuthentication,)

    # permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = {}
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class UserInfoView(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    获取当前用户信息和权限
    '''
    queryset = UserProfile.objects.all()
    serializer_class = UserInfoListSerializer
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get_permission_from_role(self, request):
        try:
            if request.user:
                perms_list = []
                for item in request.user.roles.values('permissions__method').distinct():
                    print(item)
                    perms_list.append(item['permissions__method'])
                return perms_list
        except AttributeError:
            return None


class UserBuildMenusView(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    绑定当前用户菜单信息
    '''
    queryset = UserProfile.objects.all()
    serializer_class = UserBuildMenusSerializer
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class UserViewSet(ModelViewSet):
    '''
    用户管理：增删改查
    '''
    perms_map = ({'*': 'admin'}, {'*': 'user_all'}, {'get': 'user_list'}, {'post': 'user_create'}, {'put': 'user_edit'},
                 {'delete': 'user_delete'})
    queryset = UserProfile.objects.all()
    serializer_class = UserListSerializer
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('is_active',)
    search_fields = ('username', 'name', 'mobile', 'email')
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (RbacPermission,)

    def get_serializer_class(self):
        # 根据请求类型动态变更serializer
        print(self.action)
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'list':
            return UserListSerializer
        elif self.action == 'upload_avatar':
            return UploadAvatarSerializer
        return UserModifySerializer

    def create(self, request, *args, **kwargs):
        # 创建用户默认添加密码
        request.data['password'] = '123456'
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        # 删除用户时删除其他表关联的用户
        instance = self.get_object()
        id = str(kwargs['pk'])
        projects = Project.objects.filter(
            Q(user_id__icontains=id + ',') | Q(user_id__in=id) | Q(user_id__endswith=',' + id)).values()
        if projects:
            for project in projects:
                user_id = project['user_id'].split(',')
                user_id.remove(id)
                user_id = ','.join(user_id)
                Project.objects.filter(id=project['id']).update(user_id=user_id)
        ConnectionInfo.objects.filter(uid_id=id).delete()
        self.perform_destroy(instance)
        return Response(status=NO_CONTENT)

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated],
            url_path='change-passwd', url_name='change-passwd')
    def set_password(self, request, pk=None):
        perms = UserInfoView.get_permission_from_role(request)
        user = UserProfile.objects.get(id=pk)
        if 'admin' in perms or 'user_all' in perms or request.user.is_superuser:
            serializer = ChangePasswdAdminSerializer(request.data)
            serializer.is_valid(raise_exception=True)
            user.set_password(serializer.validated_data["new_password2"])
            user.save()
            return Response('密码修改成功!')
        else:

            serializer = ChangePasswdSerializer(request.data)
            serializer.is_valid(raise_exception=True)
            user.set_password(serializer.validated_data["new_password2"])
            user.save()
            return Response('密码修改成功!')

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated],
            url_path='upload-avatar', url_name='upload-avatar')
    def upload_avatar(self, request, *args, **kwargs):
        print(request.user)
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(request.user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UserListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserListSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('name',)
    ordering_fields = ('id',)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,)
