# Generated by Django 3.0 on 2021-04-15 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20210415_1034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='coupon',
        ),
        migrations.RemoveField(
            model_name='order',
            name='transaction_id',
        ),
    ]
