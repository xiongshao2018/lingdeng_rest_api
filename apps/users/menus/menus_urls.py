'''
-*- coding: utf-8 -*-
@Author  : lingdeng
@Time    : 2020/8/25 10:34 下午
@Software: PyCharm
@File    : serializers.py
@IDE    : PyCharm
'''
from rest_framework import routers

from users.menus import views

app_name = 'menus'
router = routers.DefaultRouter()
router.register(r'index', views.MenuViewSet, basename="menus_index")
router.register(r'menus_tree', views.MenuTreeView, basename="menus_tree")

urlpatterns = router.urls
