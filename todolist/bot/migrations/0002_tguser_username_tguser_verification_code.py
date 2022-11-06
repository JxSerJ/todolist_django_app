# Generated by Django 4.1.2 on 2022-11-06 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tguser',
            name='username',
            field=models.CharField(blank=True, default=None, max_length=256, null=True, verbose_name='tg_username'),
        ),
        migrations.AddField(
            model_name='tguser',
            name='verification_code',
            field=models.CharField(max_length=16, null=True, verbose_name='verification code'),
        ),
    ]