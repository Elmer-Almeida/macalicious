# Generated by Django 3.2.9 on 2021-12-05 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_macaronimage'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MacaronImage',
            new_name='MacaronSetImage',
        ),
        migrations.AlterModelOptions(
            name='macaronsetimage',
            options={'verbose_name': 'Macaron Set Image', 'verbose_name_plural': 'Macaron Set Images'},
        ),
    ]
