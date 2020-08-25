'''
-*- coding: utf-8 -*-
@Author  : lingdeng
@Time    : 2020/8/25 10:34 下午
@Software: PyCharm
@File    : serializers.py
@IDE    : PyCharm
'''
from django.urls import path,include
from users.views import user,organization,menu,role,permission
from cmdb.views import dict
from rest_framework import routers
app_name = 'users'
router = routers.DefaultRouter()
router.register(r'users', user.UserViewSet, basename="users")
router.register(r'organizations', organization.OrganizationViewSet, basename="organization")
router.register(r'menus', menu.MenuViewSet, basename="menus")
router.register(r'permissions', permission.PermissionViewSet, basename="permissions")
router.register(r'roles', role.RoleViewSet, basename="roles")
router.register(r'dicts', dict.DictViewSet, basename="dicts")
router.register(r'login', user.UserAuthView, basename="login")
router.register(r'info', user.UserInfoView, basename="info")
router.register(r'build/menus', user.UserBuildMenusView, basename="build_menus")
router.register(r'organization/tree', organization.OrganizationTreeView, basename="organizations_tree")
router.register(r'organization/user/tree', organization.OrganizationUserTreeView, basename="organization_user_tree")
router.register(r'menu/tree', menu.MenuTreeView, basename="menus_tree")
router.register(r'permission/tree', permission.PermissionTreeView, basename="permissions_tree")
router.register(r'user/list', user.UserListView, basename="user_list")

urlpatterns = router.urls
