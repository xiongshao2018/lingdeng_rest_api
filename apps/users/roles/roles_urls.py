'''
-*- coding: utf-8 -*-
@Author  : lingdeng
@Time    : 2020/8/25 10:34 下午
@Software: PyCharm
@File    : serializers.py
@IDE    : PyCharm
'''

from rest_framework import routers

from users.roles import views

app_name = 'roles_index'
router = routers.DefaultRouter()
router.register(r'index', views.RoleViewSet, basename="roles_index")
urlpatterns = router.urls
