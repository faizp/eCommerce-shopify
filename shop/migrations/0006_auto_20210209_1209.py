# Generated by Django 3.0 on 2021-02-09 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20210209_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image1',
            field=models.ImageField(upload_to='products/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image2',
            field=models.ImageField(upload_to='products/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image3',
            field=models.ImageField(upload_to='products/%Y/%m/%d'),
        ),
    ]