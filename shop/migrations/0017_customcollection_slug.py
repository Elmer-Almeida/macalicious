# Generated by Django 3.2.9 on 2021-12-25 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_customcollection_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='customcollection',
            name='slug',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]
