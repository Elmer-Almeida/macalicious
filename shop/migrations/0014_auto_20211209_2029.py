# Generated by Django 3.2.9 on 2021-12-09 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_auto_20211208_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='macaroncollection',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Price for entire collection.', max_digits=5),
        ),
        migrations.AlterField(
            model_name='macaronset',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Price of <b>each</b> macaron. <b>NOT</b> price of entire box.', max_digits=5),
        ),
    ]