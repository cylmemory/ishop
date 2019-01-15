#!/usr/bin/env python
# encoding: utf-8

import xadmin
from .models import UserCollections, UserLeavingMessage, UserAddress


class UserCollectionsAdmin(object):
    list_display = ['user', 'goods', "add_time"]


class UserLeavingMessageAdmin(object):
    list_display = ['user', 'message_type', "msg_content", "add_time"]


class UserAddressAdmin(object):
    list_display = ["signer_name", "signer_mobile", "district", "address"]


xadmin.site.register(UserCollections, UserCollectionsAdmin)
xadmin.site.register(UserAddress, UserAddressAdmin)
xadmin.site.register(UserLeavingMessage, UserLeavingMessageAdmin)
