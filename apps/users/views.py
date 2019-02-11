# from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from random import choice
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import MsgSerializer, UserRegSerializer, UserDetailSerializer
from utils.yunpian import Yunpian
from ishop.settings import APIKEY
from .models import VerifyMessage

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


class MsgCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    send mobile msg
    """
    serializer_class = MsgSerializer

    def generate_code(self):
        """
        生成随机验证码
        :return:
        """
        num = '123456789'
        random_str = []
        for i in range(4):
            random_str.append(choice(num))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validate_data['mobile']
        yunpian = Yunpian(APIKEY)
        code = self.generate_code()
        result = yunpian.send_msg(code, mobile=mobile)

        if result["code"] != 0:
            return Response({
                "mobile": result["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyMessage(code=code, mobile=mobile)
            code_record.save()

            return Response({
                "mobile": mobile
            }, status.HTTP_201_CREATED)


class UserViewset(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户注册
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 重写获取serializer函数是为了判断在API获取用户信息或者创建用户时使用那个序列化类进行对字段的序列化
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer

    # 重写获取权限函数,主要用于在判断创建和修改用户信息时,是否需要登录权限
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        pay_load = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(pay_load)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
