# Generated by Django 3.2 on 2023-01-03 22:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Category name')),
                ('slug', models.SlugField(unique=True, validators=[django.core.validators.RegexValidator(regex='^[-a-zA-Z0-9_]+$')], verbose_name='Category slug')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Genre name')),
                ('slug', models.SlugField(unique=True, validators=[django.core.validators.RegexValidator(regex='^[-a-zA-Z0-9_]+$')], verbose_name='Genre slug')),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='default name', max_length=256, verbose_name='Name of art work')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Short description')),
                ('year', models.IntegerField(validators=[django.core.validators.MinValueValidator(-500000), django.core.validators.MaxValueValidator(2023)], verbose_name='Creation year')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category', verbose_name='Category')),
                ('genre', models.ManyToManyField(blank=True, related_name='titles', to='reviews.Genre', verbose_name='Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Review text')),
                ('score', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Score of the title')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Publication date')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.title')),
            ],
            options={
                'unique_together': {('title', 'author')},
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Сomment text')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Publication date')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='сomments', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='сomments', to='reviews.review')),
            ],
        ),
    ]
