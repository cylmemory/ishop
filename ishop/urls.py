"""ishop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.urls import path
from django.urls import include
from ishop.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from goods.views import GoodsListViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'goods', GoodsListViewSet, base_name='Goods')

# goods_list = GoodsListViewSet.as_view({
#     'get': 'list'
# })

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    # path('goods/', goods_list, name="goods-list"),
    path('', include(router.urls)),
    # doc
    path('docs/', include_docs_urls(title="online shop")),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
