# Generated by Django 3.2.9 on 2021-12-05 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20211205_1737'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MacaronSetImage',
            new_name='MacaronImage',
        ),
        migrations.AlterModelOptions(
            name='macaronimage',
            options={'verbose_name': 'Macaron Image', 'verbose_name_plural': 'Macaron Images'},
        ),
    ]
