# Generated by Django 3.0 on 2021-03-23 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20210323_2234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='name',
        ),
        migrations.RemoveField(
            model_name='coupon',
            name='user',
        ),
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(max_length=16, unique=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Category'),
        ),
    ]
