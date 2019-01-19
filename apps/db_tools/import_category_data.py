#!/usr/bin/env python
# -*- coding:utf-8 -*-


# 独立使用django的model

import sys
import os

# 获取当前文件的路径
pwd = os.path.dirname(os.path.realpath(__file__))
# 获取项目的跟目录
sys.path.append(pwd + "../")

# 要想单独使用django的model，必须指定一个环境变量，在manage.py或wsgi.py中找
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ishop.settings')

import django

django.setup()

from goods.models import GoodsCategory
from db_tools.data.category_data import row_data

# 1级分类
for level1_cat in row_data:
    category1 = GoodsCategory()
    category1.name_en = level1_cat["code"]
    category1.name = level1_cat["name"]
    category1.category_level = 1
    category1.save()

    # 二级分类
    for level2_cat in level1_cat["sub_categorys"]:
        category2 = GoodsCategory()
        category2.name_en = level2_cat["code"]
        category2.name = level2_cat["name"]
        category2.category_level = 2
        category2.parent_category = category1
        category2.save()

        # 三级分类
        for level3_cat in level2_cat["sub_categorys"]:
            category3 = GoodsCategory()
            category3.name_en = level2_cat["code"]
            category3.name = level2_cat["name"]
            category3.category_level = 3
            category3.parent_category = category2
            category3.save()
