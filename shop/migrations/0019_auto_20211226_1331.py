# Generated by Django 3.2.9 on 2021-12-26 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_auto_20211226_1324'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customcollectiontype',
            options={'verbose_name': 'Macaron Custom Collection Type', 'verbose_name_plural': 'Macaron Custom Collection Types'},
        ),
        migrations.RenameField(
            model_name='customcollectiontype',
            old_name='quantity',
            new_name='quantity_total',
        ),
        migrations.RemoveField(
            model_name='customcollection',
            name='quantity',
        ),
        migrations.AddField(
            model_name='customcollectiontype',
            name='quantity_each',
            field=models.PositiveIntegerField(default=3, help_text='Quantity for each flavor in the collection'),
        ),
    ]