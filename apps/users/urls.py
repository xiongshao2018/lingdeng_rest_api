from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from cmdb.views import dict
from users.users import users_urls
from users.views import organization, menu, role, permission

app_name = 'users'
router = routers.DefaultRouter()
router.register(r'organizations', organization.OrganizationViewSet, basename="organization")
router.register(r'menus', menu.MenuViewSet, basename="menus")
router.register(r'permissions', permission.PermissionViewSet, basename="permissions")
router.register(r'roles', role.RoleViewSet, basename="roles")
router.register(r'dicts', dict.DictViewSet, basename="dicts")
router.register(r'organization/tree', organization.OrganizationTreeView, basename="organizations_tree")
router.register(r'organization/user/tree', organization.OrganizationUserTreeView, basename="organization_user_tree")
router.register(r'menu/tree', menu.MenuTreeView, basename="menus_tree")
router.register(r'permission/tree', permission.PermissionTreeView, basename="permissions_tree")

urlpatterns = [
    url(r'^users/', include(users_urls, namespace='users_index')),  # 用户app
    url(r'^', include(router.urls)),  # 用户app
]
