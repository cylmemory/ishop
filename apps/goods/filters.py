# -*- coding:utf-8 -*-


from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Goods


class GoodsFilter(filters.FilterSet):
    """
    商品过滤类
    """
    min_price = filters.NumberFilter(field_name='sale_price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='sale_price', lookup_expr='lte')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    top_category = filters.NumberFilter(method="top_category_filter")

    # 点击任何一级二级三级分类，都可以过滤出对应分类的商品的方法，value指传递category的id
    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) |
                               Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['min_price', 'max_price', 'name']
