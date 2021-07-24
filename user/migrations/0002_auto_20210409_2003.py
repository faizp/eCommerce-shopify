# Generated by Django 3.0 on 2021-04-09 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='refer',
            field=models.CharField(default='REFER', max_length=10, unique=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='refer_by',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
