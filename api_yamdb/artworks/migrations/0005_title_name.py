# Generated by Django 3.2 on 2022-12-28 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0004_auto_20221228_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='name',
            field=models.TextField(default='default_name', verbose_name='Название'),
            preserve_default=False,
        ),
    ]
