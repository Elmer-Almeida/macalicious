# Generated by Django 3.2.9 on 2021-12-23 16:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0006_auto_20211223_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('macarons', models.ManyToManyField(limit_choices_to={'active': True}, to='shop.CustomCollectionItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Macaron Custom Collection',
                'verbose_name_plural': 'Macaron Custom Collections',
            },
        ),
    ]
