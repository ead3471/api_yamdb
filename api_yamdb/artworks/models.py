from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator,
                                    RegexValidator)
from datetime import datetime

User = get_user_model()


class Category(models.Model):
    name = models.CharField(verbose_name="Category name",
                            max_length=256)
    slug = models.SlugField(verbose_name="Category slug",
                            max_length=50,
                            unique=True,
                            validators=[
                                RegexValidator(regex="^[-a-zA-Z0-9_]+$")
                            ])

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name="Genre name",
                            max_length=256)
    slug = models.SlugField(verbose_name="Genre slug",
                            max_length=50,
                            unique=True,
                            validators=[
                                RegexValidator(regex="^[-a-zA-Z0-9_]+$")
                            ])

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    MINIMUM_TITLE_YEAR = -500000  # The first known work of art

    name = models.CharField(verbose_name="Name of art work",
                            max_length=256,
                            default='default name')

    description = models.TextField(verbose_name="Short description",
                                   null=True,
                                   blank=True)

    rating = models.DecimalField(verbose_name="Raiting",
                                 max_digits=2,
                                 decimal_places=1,
                                 default=0)

    year = models.IntegerField(verbose_name="Creation year",
                               validators=[
                                   MinValueValidator(MINIMUM_TITLE_YEAR),
                                   MaxValueValidator(
                                       lambda: datetime.now().year)],
                               )

    category = models.ForeignKey(Category,
                                 verbose_name='Category',
                                 null=True,
                                 related_name='titles',
                                 on_delete=models.SET_NULL)

    genre = models.ManyToManyField(Genre,
                                   verbose_name='Genre',
                                   related_name="titles",
                                   blank=True,
                                   )

    def __str__(self) -> str:
        return self.name
