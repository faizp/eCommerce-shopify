# Generated by Django 3.0 on 2021-03-19 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20210319_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Size'),
        ),
    ]
