# Generated by Django 3.2.9 on 2021-12-23 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_customcollectionitem_quantity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customcollectiontype',
            options={'verbose_name': 'Macaron Custom Collection Type', 'verbose_name_plural': 'Macaron Custom Collection Types'},
        ),
        migrations.AlterField(
            model_name='customcollection',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
