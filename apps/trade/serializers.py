# -*- coding:utf-8 -*-
from random import Random
import time
from rest_framework import serializers

from goods.models import Goods
from trade.models import ShoppingCart, OrderInfo, OrderGoods
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


class OrderSerializer(serializers.ModelSerializer):
    """
    订单序列化类
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_no = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    post_script = serializers.CharField(read_only=True)
    pay_type = serializers.CharField(read_only=True)

    # 生成订单
    def generate_order_no(self):
        random_ins = Random()
        order_no = "{time_str}{user_id}{random_no}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                           user_id=self.context["request"].user.id,
                                                           random_no=random_ins.randint(10, 99))
        return order_no

    def validate(self, attrs):
        attrs["order_no"] = self.generate_order_no()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderGoodsSerializer(serializers.ModelSerializer):
    """
    订单货品序列化类
    """
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    订单明细序列化类
    """
    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = '__all__'


