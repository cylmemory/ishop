# -*- coding:utf-8 -*-

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import UserCollections


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

