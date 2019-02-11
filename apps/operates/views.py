from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, AddressManageSerializer
from .models import UserCollections, UserLeavingMessage, UserAddress
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取收藏列表信息
    create：
        收藏货品
    destroy:
        取消收藏
    retrieve:
        判断某个货品是否收藏
    """
    lookup_field = "goods_id"
    serializer_class = UserFavSerializer
    # 认证方式类
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 权限类
    # IsAuthenticated：必须登录用户；IsOwnerOrReadOnly：必须是当前登录的用户
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return UserCollections.objects.filter(user=self.request.user)

    # 动态序列化类
    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer

        return UserFavSerializer


class LeavingMessageViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    """
    list:
        获取留言
    create:
        新增留言
    destroy:
        删除留言
    """
    serializer_class = LeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressManageViewSet(viewsets.ModelViewSet):
    """
    list:
        获取收货地址
    create:
        新增收货地址
    destroy:
        删除收货地址
    update:
        更新收货地址
    retrieve:
        验证是否存在某个收货地址


    """
    serializer_class = AddressManageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
