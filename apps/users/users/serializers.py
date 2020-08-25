'''
-*- coding: utf-8 -*-
@Author  : lingdeng
@Time    : 2020/8/25 10:34 下午
@Software: PyCharm
@File    : serializers.py
@IDE    : PyCharm
'''
# @Time    : 2019/1/14 15:11
# @Author  : xufqing
import re
from operator import itemgetter

from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import serializers

from ..models import UserProfile, Menu
from ..serializers.menu_serializer import MenuSerializer


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, min_length=5, max_length=20, label="用户名", help_text="用户名",
                                     error_messages={'min_length': '用户名不能小于5个字符', 'max_length': '用户名不能大于20个字符',
                                                     'required': '请填写用户名'})
    password = serializers.CharField(required=True, min_length=6, max_length=18, label="密码", help_text="密码",
                                     style={'input_type': 'password'},
                                     error_messages={'min_length': '密码不能小于6个字符', 'max_length': '密码不能大于18个字符',
                                                     'required': '请填写密码'})

    def validate(self, attrs):
        # 登录账户
        user = UserProfile.objects.filter(Q(username=attrs["username"]) | Q(email=attrs["username"])).first()
        if user is not None:
            if not user.check_password(attrs["password"]):
                raise serializers.ValidationError({"password": "密码错误"})
        else:
            raise serializers.ValidationError({"username": "用户不存在"})
        return attrs

    def create(self, validated_data):
        # 登录账户
        user = authenticate(username=validated_data["username"], password=validated_data["password"])
        return user


class UserListSerializer(serializers.ModelSerializer):
    '''
    用户列表的序列化
    '''
    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        return obj.roles.values()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'name', 'mobile', 'email', 'image', 'department', 'position', 'superior',
                  'is_active', 'roles']
        depth = 1


class UserModifySerializer(serializers.ModelSerializer):
    '''
    用户编辑的序列化
    '''
    mobile = serializers.CharField(max_length=11)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'name', 'mobile', 'email', 'image', 'department', 'position', 'superior',
                  'is_active', 'roles']

    def validate_mobile(self, mobile):
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不合法")
        return mobile


class UserCreateSerializer(serializers.ModelSerializer):
    '''
    创建用户序列化
    '''
    username = serializers.CharField(required=True, allow_blank=False)
    mobile = serializers.CharField(max_length=11)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'name', 'mobile', 'email', 'department', 'position', 'is_active', 'roles',
                  'password']

    def validate_username(self, username):
        if UserProfile.objects.filter(username=username):
            raise serializers.ValidationError(username + ' 账号已存在')
        return username

    def validate_mobile(self, mobile):
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不合法")
        if UserProfile.objects.filter(mobile=mobile):
            raise serializers.ValidationError("手机号已经被注册")
        return mobile


class UserInfoListSerializer(serializers.ModelSerializer):
    '''
    公共users
    '''
    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        try:
            if obj.roles:
                perms_list = []
                for item in obj.roles.values('permissions__method').distinct():
                    perms_list.append(item['permissions__method'])
                return perms_list
        except AttributeError:
            return None

    class Meta:
        model = UserProfile
        fields = ('id', 'name', 'mobile', 'image', 'email', 'roles')


class UserBuildMenusSerializer(serializers.ModelSerializer):
    '''
    公共users
    '''
    roles = serializers.SerializerMethodField()

    def get_menu_from_role(self, obj):
        if obj:
            menu_dict = {}
            menus = obj.roles.values(
                'menus__id',
                'menus__name',
                'menus__path',
                'menus__is_frame',
                'menus__is_show',
                'menus__component',
                'menus__icon',
                'menus__sort',
                'menus__pid'
            ).distinct()
            for item in menus:
                if item['menus__pid'] is None:
                    if item['menus__is_frame']:
                        # 判断是否外部链接
                        top_menu = {
                            'id': item['menus__id'],
                            'path': item['menus__path'],
                            'component': 'Layout',
                            'children': [{
                                'path': item['menus__path'],
                                'meta': {
                                    'title': item['menus__name'],
                                    'icon': item['menus__icon']
                                }
                            }],
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort']
                        }
                    else:
                        top_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': '/' + item['menus__path'],
                            'redirect': 'noredirect',
                            'component': 'Layout',
                            'alwaysShow': True,
                            'meta': {
                                'title': item['menus__name'],
                                'icon': item['menus__icon']
                            },
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort'],
                            'children': []
                        }
                    menu_dict[item['menus__id']] = top_menu
                else:
                    if item['menus__is_frame']:
                        children_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': item['menus__path'],
                            'component': 'Layout',
                            'meta': {
                                'title': item['menus__name'],
                                'icon': item['menus__icon'],
                            },
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort']
                        }
                    elif item['menus__is_show']:
                        children_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': item['menus__path'],
                            'component': item['menus__component'],
                            'meta': {
                                'title': item['menus__name'],
                                'icon': item['menus__icon'],
                            },
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort']
                        }
                    else:
                        children_menu = {
                            'id': item['menus__id'],
                            'name': item['menus__name'],
                            'path': item['menus__path'],
                            'component': item['menus__component'],
                            'meta': {
                                'title': item['menus__name'],
                                'noCache': True,
                            },
                            'hidden': True,
                            'pid': item['menus__pid'],
                            'sort': item['menus__sort']
                        }
                    menu_dict[item['menus__id']] = children_menu
            return menu_dict

    def get_all_menu_dict(self):
        '''
        获取所有菜单数据，重组结构
        '''
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        tree_dict = {}
        for item in serializer.data:
            if item['pid'] is None:
                if item['is_frame']:
                    # 判断是否外部链接
                    top_menu = {
                        'id': item['id'],
                        'path': item['path'],
                        'component': 'Layout',
                        'children': [{
                            'path': item['path'],
                            'meta': {
                                'title': item['name'],
                                'icon': item['icon']
                            }
                        }],
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                else:
                    top_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': '/' + item['path'],
                        'redirect': 'noredirect',
                        'component': 'Layout',
                        'alwaysShow': True,
                        'meta': {
                            'title': item['name'],
                            'icon': item['icon']
                        },
                        'pid': item['pid'],
                        'sort': item['sort'],
                        'children': []
                    }
                tree_dict[item['id']] = top_menu
            else:
                if item['is_frame']:
                    children_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': item['path'],
                        'component': 'Layout',
                        'meta': {
                            'title': item['name'],
                            'icon': item['icon'],
                        },
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                elif item['is_show']:
                    children_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': item['path'],
                        'component': item['component'],
                        'meta': {
                            'title': item['name'],
                            'icon': item['icon'],
                        },
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                else:
                    children_menu = {
                        'id': item['id'],
                        'name': item['name'],
                        'path': item['path'],
                        'component': item['component'],
                        'meta': {
                            'title': item['name'],
                            'noCache': True,
                        },
                        'hidden': True,
                        'pid': item['pid'],
                        'sort': item['sort']
                    }
                tree_dict[item['id']] = children_menu
        return tree_dict

    def get_roles(self, obj):
        try:
            if obj.roles:
                perms_list = []
                for item in obj.roles.values('permissions__method').distinct():
                    print(item['permissions__method'])
                    perms_list.append(item['permissions__method'])

                tree_data = []
                if 'admin' in perms_list or obj.is_superuser:
                    tree_dict = self.get_all_menu_dict()
                else:
                    tree_dict = self.get_menu_from_role(obj)
                for i in tree_dict:
                    if tree_dict[i]['pid']:
                        pid = tree_dict[i]['pid']
                        parent = tree_dict[pid]
                        parent.setdefault('redirect', 'noredirect')
                        parent.setdefault('alwaysShow', True)
                        parent.setdefault('children', []).append(tree_dict[i])
                        parent['children'] = sorted(parent['children'], key=itemgetter('sort'))
                    else:
                        tree_data.append(tree_dict[i])

                return tree_data
        except AttributeError:
            return None

    class Meta:
        model = UserProfile
        fields = ('roles',)


class ChangePasswdSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, min_length=6, max_length=18, write_only=True,
                                         style={'input_type': 'password'}, label="旧密码", help_text="旧密码",
                                         error_messages={'min_length': '密码不能小于6个字符', 'max_length': '密码不能大于18个字符',
                                                         'required': '请填写密码'})
    new_password1 = serializers.CharField(required=True, min_length=6, max_length=18, write_only=True,
                                          style={'input_type': 'password'}, label="新密码", help_text="新密码",
                                          error_messages={'min_length': '密码不能小于6个字符', 'max_length': '密码不能大于18个字符',
                                                          'required': '请填写密码'})
    new_password2 = serializers.CharField(required=True, min_length=6, max_length=18, style={'input_type': 'password'},
                                          label="确认密码", help_text="确认密码",
                                          error_messages={'min_length': '密码不能小于6个字符', 'max_length': '密码不能大于18个字符',
                                                          'required': '请填写密码'}, write_only=True)

    def validate_old_password(self, old_password):
        """
        验证密码是否一致
        :param attrs:
        :return:
        """
        # 验证密码
        username = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            username = request.user

        user = UserProfile.objects.get(username=username)
        print(user.check_password(old_password))
        if user.check_password(old_password) is False:
            raise serializers.ValidationError("密码不正确")

    def validate_new_password2(self, new_password2):
        """
        验证密码是否一致
        :param attrs:
        :return:
        """
        # 验证密码
        if self.initial_data["new_password1"] != new_password2:
            raise serializers.ValidationError("密码输入不一致")

        return new_password2


class ChangePasswdAdminSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(required=True, min_length=6, max_length=18, write_only=True,
                                          style={'input_type': 'password'}, label="新密码", help_text="新密码",
                                          error_messages={'min_length': '密码不能小于6个字符', 'max_length': '密码不能大于18个字符',
                                                          'required': '请填写密码'})
    new_password2 = serializers.CharField(required=True, min_length=6, max_length=18, style={'input_type': 'password'},
                                          label="确认密码", help_text="确认密码",
                                          error_messages={'min_length': '密码不能小于6个字符', 'max_length': '密码不能大于18个字符',
                                                          'required': '请填写密码'}, write_only=True)

    def validate_new_password2(self, new_password2):
        """
        验证密码是否一致
        :param attrs:
        :return:
        """
        # 验证密码
        if self.initial_data["new_password1"] != new_password2:
            raise serializers.ValidationError("密码输入不一致")

        return new_password2


class UploadAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ["image"]
