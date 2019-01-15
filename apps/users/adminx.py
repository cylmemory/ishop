#!/usr/bin/env python
# encoding: utf-8

import xadmin
from xadmin import views
from .models import VerifyMessage


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "生鲜网站后台"
    site_footer = "ishop"
    # menu_style = "accordion"


class VerifyMessageAdmin(object):
    list_display = ['code', 'mobile', "add_time"]


xadmin.site.register(VerifyMessage, VerifyMessageAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)