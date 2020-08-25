'''
-*- coding: utf-8 -*-
@Author  : lingdeng
@Time    : 2020/8/25 10:34 下午
@Software: PyCharm
@File    : serializers.py
@IDE    : PyCharm
'''
from rest_framework import routers

from users.permission import views

app_name = 'permissions_index'
router = routers.DefaultRouter()

router.register(r'index', views.PermissionViewSet, basename="permissions_index")
router.register(r'permission_tree', views.PermissionTreeView, basename="permissions_tree")

urlpatterns = router.urls
