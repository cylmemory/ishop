# -*- coding:utf-8 -*-
import re
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import UserCollections, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer



class UserFavSerializer(serializers.ModelSerializer):
    """
    收藏功能序列化类
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserCollections
        # 用于验证重复
        validators = [
            UniqueTogetherValidator(
                queryset=UserCollections.objects.all(),
                fields=('user', 'goods'),
                message="已收藏"
            )
        ]
        fields = ('user', 'goods', 'id')


class UserFavDetailSerializer(serializers.ModelSerializer):
    """
    收藏货品详情序列化类
    """
    goods = GoodsSerializer()

    class Meta:
        model = UserCollections
        fields = ('goods', 'id')


class LeavingMessageSerializer(serializers.ModelSerializer):
    """
    用户留言功能序列化类
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserLeavingMessage
        fields = ('id', 'user', 'message_type', 'subject', 'msg_content', 'file', 'add_time')


REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"


class AddressManageSerializer(serializers.ModelSerializer):
    """
    用户留言功能序列化类
    """

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    province = serializers.CharField(required=True, error_messages={
        "required": "省份不能为空",
    })

    city = serializers.CharField(required=True, error_messages={
        "required": "城市不能为空",
    })

    district = serializers.CharField(required=True, error_messages={
        "required": "区域不能为空",
    })
    signer_name = serializers.CharField(required=True, max_length=50)

    address = serializers.CharField(required=True, error_messages={
        "required": "详细地址不能为空",
    })

    signer_mobile = serializers.CharField(required=True, error_messages={
        "required": "手机号码不能为空",
    })

    def validate_signer_mobile(self, signer_mobile):
        """
        验证手机号
        :param mobile:
        :return:
        """

        if not re.match(REGEX_MOBILE, signer_mobile):
            raise serializers.ValidationError("请输入正确的手机号")

        return signer_mobile

    class Meta:
        model = UserAddress
        fields = ('id', 'user', 'province', 'city', 'district', 'address', 'signer_name', 'signer_mobile',
                  'add_time')

