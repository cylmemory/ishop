# -*- coding:utf-8 -*-

# from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()


# receiver是接收器，sender表示是从哪个数据库中传过来,created=False表示是否是新建的时候发送信号，instance表示User
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
        # Token.objects.create(user=instance)
