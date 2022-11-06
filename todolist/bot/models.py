from django.db import models


class TgUser(models.Model):
    tg_user_id = models.BigIntegerField(verbose_name='tg_id', unique=True)
    tg_chat_id = models.BigIntegerField(verbose_name='tg_chat_id')
    user_id = models.ForeignKey(verbose_name='internal user',
                                to='core.User',
                                on_delete=models.PROTECT,
                                null=True,
                                blank=True,
                                default=None)
