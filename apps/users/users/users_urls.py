'''
-*- coding: utf-8 -*-
@Author  : lingdeng
@Time    : 2020/8/25 10:34 下午
@Software: PyCharm
@File    : serializers.py
@IDE    : PyCharm
'''
from rest_framework import routers

from cmdb.views import dict
from users.users import views

app_name = 'users_index'
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename="users")
router.register(r'login', views.UserAuthView, basename="login")
router.register(r'info', views.UserInfoView, basename="info")
router.register(r'build_menus', views.UserBuildMenusView, basename="build_menus")
router.register(r'user_list', views.UserListView, basename="user_list")
urlpatterns = router.urls
