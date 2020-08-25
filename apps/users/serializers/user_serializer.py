# @Time    : 2019/1/14 15:11
# @Author  : xufqing
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import serializers
from ..models import UserProfile, Role, Permission
import re

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
                  'is_active','roles']
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

class permissionsSerializer(serializers.ModelSerializer):
    '''
    公共users
    '''
    class Meta:
        model = Permission
        fields = ("method",)

class RoleSerializer(serializers.ModelSerializer):
    '''
    公共users
    '''
    permissions  = permissionsSerializer(many=True)
    def validate_permissions(self, permissions):
        print(permissions)
        return permissions
    class Meta:
        model = Role
        fields = ("permissions",)

class UserInfoListSerializer(serializers.ModelSerializer):
    '''
    公共users
    '''
    roles = RoleSerializer(many=True)

    def validate_roles(self, roles):
        print(roles)
        return roles
    class Meta:
        model = UserProfile
        fields = ('id','name','mobile','image','email','roles')