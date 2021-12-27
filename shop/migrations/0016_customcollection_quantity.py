# Generated by Django 3.2.9 on 2021-12-25 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_customcollection_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='customcollection',
            name='quantity',
            field=models.PositiveIntegerField(default=3, help_text='Quantity for each flavor'),
        ),
    ]