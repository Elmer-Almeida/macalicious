# Generated by Django 3.2.9 on 2021-12-04 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Cart', 'verbose_name_plural': 'Carts'},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'Cart Item', 'verbose_name_plural': 'Cart Items'},
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='item',
            new_name='item_type',
        ),
    ]
