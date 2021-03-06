from django.shortcuts import render


from rest_framework import generics
from rest_framework import mixins
from .models import Goods, GoodsCategory
from rest_framework.pagination import PageNumberPagination

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter
from rest_framework import filters
from .serializers import GoodsSerializer, CategorySerializer


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        category list data
    retrieve:
        get category details
    """
    queryset = GoodsCategory.objects.filter(category_level=1)
    serializer_class = CategorySerializer


class GoodsPagination(PageNumberPagination):
    """
    pagination
    """
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


# class GoodsListView(generics.ListAPIView), GenericView没有action(post,get)方法，所以还有继承ListModelMixin
class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    List All Goods
    """
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    queryset = Goods.objects.all().order_by("id")
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_fields = ('name', 'sale_price')
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'sale_price')
    # def get_queryset(self):
    #     return Goods.objects.filter(sale_price__gt=100).order_by('id')
