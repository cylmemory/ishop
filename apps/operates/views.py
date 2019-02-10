from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .serializers import UserFavSerializer
from .models import UserCollections
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    user goods collections
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

