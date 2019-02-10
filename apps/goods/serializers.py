# -*- coding:utf-8 -*-

from rest_framework import serializers
from .models import Goods, GoodsCategory, GoodsImage


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


class GoodsImageSerializers(serializers.ModelSerializer):
    """
    商品轮播图序列化类
    """
    class Meta:
        model = GoodsImage
        fields = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
    """
    商品序列化类
    """
    category = CategorySerializer()
    images = GoodsImageSerializers(many=True)

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
