# -*- coding:utf-8 -*-
import re
from _datetime import datetime, timedelta

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import VerifyMessage


User = get_user_model()
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"


class MsgSerializer(serializers.Serializer):
    """
    注册提交验证码序列化类
    """
    mobile = serializers.CharField(max_length=11)
    def validate_mobile(self, mobile):
        """
        验证手机号
        :param mobile:
        :return:
        """
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("此手机已经注册！")

        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号无效")

        add_time= datetime.now()- timedelta(hours=0, minutes=1, seconds=0)
        if VerifyMessage.objects.filter(add_time__gt=add_time, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

         return mobile