# Generated by Django 3.0 on 2021-04-15 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20210415_1037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='valid',
        ),
    ]