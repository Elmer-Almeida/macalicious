# Generated by Django 3.2.9 on 2021-12-23 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_rename_customcollectiondeclaration_customcollectiontype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customcollectionitem',
            name='quantity',
            field=models.PositiveIntegerField(default=3),
        ),
    ]