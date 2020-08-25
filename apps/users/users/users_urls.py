'''
-*- coding: utf-8 -*-
@Author  : lingdeng
@Time    : 2020/8/25 10:34 下午
@Software: PyCharm
@File    : serializers.py
@IDE    : PyCharm
'''
from rest_framework import routers

from users.users import views

app_name = 'users_index'
router = routers.DefaultRouter()
router.register(r'index', views.UserViewSet, basename="users_index")
router.register(r'login', views.UserAuthView, basename="users_login")
router.register(r'info', views.UserInfoView, basename="users_info")
router.register(r'build_menus', views.UserBuildMenusView, basename="users_build_menus")
router.register(r'user_list', views.UserListView, basename="user_list")
urlpatterns = router.urls
