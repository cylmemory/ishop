from django.shortcuts import render

from .serializers import GoodsSerializer
from rest_framework import generics
from rest_framework import mixins
from .models import Goods
from rest_framework.pagination import PageNumberPagination

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter
from rest_framework import filters


class GoodsPagination(PageNumberPagination):
    """
    pagination
    """
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100


# class GoodsListView(generics.ListAPIView), GenericView没有action(post,get)方法，所以还有继承ListModelMixin
class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List All Goods
    """
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    queryset = Goods.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_fields = ('name', 'sale_price')
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'add_time')
    # def get_queryset(self):
    #     return Goods.objects.filter(sale_price__gt=100).order_by('id')
