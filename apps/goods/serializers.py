# -*- coding:utf-8 -*-

from rest_framework import serializers
from .models import Goods, GoodsCategory


class CategorySerializer3(serializers.ModelSerializer):
    """
    三级类别
    """
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    """
    二级类别
    """
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    一级类别
    """
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Goods
        fields = '__all__'

    def create(self, validated_data):
        """
        new a goods instance
        :param validated_data:
        :return:
        """
        return Goods.objects.create(**validated_data)
