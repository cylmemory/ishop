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
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from goods.views import GoodsListViewSet, CategoryViewSet
from users.views import MsgCodeViewset, UserViewset
from operates.views import UserFavViewSet, LeavingMessageViewSet, AddressManageViewSet
from trade.views import ShoppingCartViewSet, OrderViewSet

router = DefaultRouter()

# 商品的urls
router.register(r'goods', GoodsListViewSet, base_name='Goods')
# 商品类别的urls
router.register(r'categories', CategoryViewSet, base_name='categories')

# 手机验证码url
router.register(r'codes', MsgCodeViewset, base_name='codes')

# 用户注册
router.register(r'users', UserViewset, base_name="users")

# 用户收藏
router.register(r'userfavs', UserFavViewSet, base_name='userfavs')

# 用户留言
router.register(r'messages', LeavingMessageViewSet, base_name='massages')

# 配置收货地址
router.register(r'address', AddressManageViewSet, base_name="address")

# 购物车
router.register(r'shopcarts', ShoppingCartViewSet, base_name='shopcarts')

# 订单
router.register(r'orders', OrderViewSet, base_name='orders')

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
    # test api
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # django rest framework Token authenticate model
    path('api-token-auth/', views.obtain_auth_token),
    # django rest framework json web token(jwt),
    path('login/', obtain_jwt_token)
]
