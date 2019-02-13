# -*- coding:utf-8 -*-

from rest_framework import serializers

from goods.models import Goods
from trade.models import ShoppingCart
from goods.serializers import GoodsSerializer


# serializers.Serializer是为了灵活性更强,不会报货品记录重复的错误
class ShopCartSerializer(serializers.Serializer):
    """
    购物车序列化类
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1, label="数量", error_messages={
        "min_value": "数量必须大于等于1",
        "required": "数量不能为空"
    })
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all(), label="货品", required=True)

    # validated_data是已经验证后的字段数据
    # initial_data是初始数据
    def create(self, validated_data):
        # 获取当前用户
        # view中:self.request.user；serializer中:self.context["request"].user
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        is_existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if is_existed:
            # 存在,更新数量
            is_existed = is_existed[0]
            is_existed.nums += nums
            is_existed.save()
        else:
            # 不存在，即创建
            is_existed = ShoppingCart.objects.create(**validated_data)

        return is_existed

    # 更新操作
    def update(self, instance, validated_data):
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False,)

    class Meta:
        model = ShoppingCart
        fields = ('goods', 'nums')
