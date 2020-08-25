from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from cmdb.views import dict
from users.menus import menus_urls
from users.organization import organization_urls
from users.permission import permissions_urls
from users.roles import roles_urls
from users.users import users_urls

app_name = 'users'
router = routers.DefaultRouter()
router.register(r'dicts', dict.DictViewSet, basename="dicts")

urlpatterns = [
    url(r'^auth/', include(users_urls, namespace='auth')),  # 用户
    url(r'^menus/', include(menus_urls, namespace='menus')),  # 菜单
    url(r'^roles/', include(roles_urls, namespace='roles')),  # 用户组
    url(r'^permissions/', include(permissions_urls, namespace='permissions')),  # 权限
    url(r'^organizations/', include(organization_urls, namespace='organization')),  # 部门
    url(r'^dicts/', include(router.urls)),  # 权限
]
