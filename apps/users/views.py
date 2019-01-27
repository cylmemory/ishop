from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    用户自定义验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 用户名or手机号登录
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
