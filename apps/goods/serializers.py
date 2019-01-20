# -*- coding:utf-8 -*-

from rest_framework import serializers
from .models import Goods, GoodsCategory


class CategorySerlizer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerlizer()

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
