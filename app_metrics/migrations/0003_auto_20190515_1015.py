# Generated by Django 2.2 on 2019-05-15 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_metrics', '0002_auto_20190514_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gauge',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='gauge',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='updated'),
        ),
    ]