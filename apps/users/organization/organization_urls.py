'''
-*- coding: utf-8 -*-
@Author  : lingdeng
@Time    : 2020/8/25 10:34 下午
@Software: PyCharm
@File    : serializers.py
@IDE    : PyCharm
'''
from rest_framework import routers

from users.organization import views

app_name = 'organization_index'
router = routers.DefaultRouter()
router.register(r'index', views.OrganizationViewSet, basename="organization_index")
router.register(r'organizations_tree', views.OrganizationTreeView, basename="organizations_tree")
router.register(r'organizations_user_tree', views.OrganizationUserTreeView, basename="organizations_user_tree")

urlpatterns = router.urls
