from django.conf.urls import url
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from django.views.static import serve
urlpatterns = [
    url(r'^users/', include('users.urls', namespace='users')),  # 用户app
    url(r'', include('cmdb.urls')),
    url(r'', include('deployment.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('^docs/', include_docs_urls()),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),  # 图片静态链接# 接口文档
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
