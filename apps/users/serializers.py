# -*- coding:utf-8 -*-
import re
from _datetime import datetime, timedelta
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from users.models import VerifyMessage


User = get_user_model()
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"


# serializers.Serializer是为了灵活性更强,不会报记录重复的错误
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

        add_time = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyMessage.objects.filter(add_time__gt=add_time, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    """
    user detail serializer
    """
    class Meta:
        model = User
        fields = ('name', 'gender', 'birth', 'email', 'mobile')


class UserRegSerializer(serializers.ModelSerializer):
    # write_only设置为True是为了不把code这个字段序列化
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="验证码",
                                 error_messages={
                                   "blank": "请输入验证码",
                                   "required": "验证码不能为空",
                                   "max_length": "验证码错误",
                                   "min_length": "验证码错误"
                                 },
                                 help_text="验证码")
    # 验证username字段
    username = serializers.CharField(required=True, allow_blank=False, label="用户名",
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已存在")])

    password = serializers.CharField(write_only=True,  label='密码', style={'input_type': 'password'})

    # 重载create方法目的是为了把密码变成加密的形式存储在数据库中
    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_code(self, code):
        # 注册时，post的数据是都保存在initial_data中，username就用户注册手机号，记得要排序取最新的code
        verify_record = VerifyMessage.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_record:
            # 取最新的验证码
            last_record = verify_record[0]
            five_minute_limit = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

            if five_minute_limit > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
        else:
            raise serializers.ValidationError("请确认账号")

    # attrs是要验证的所有的字段
    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password')

