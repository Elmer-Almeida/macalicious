# Generated by Django 3.2.9 on 2021-12-12 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='macaroncollection',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='macaronimage',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
