from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User


class Title(models.Model):
    name = models.TextField(verbose_name="Название")
    description = models.TextField(verbose_name="Краткое описание",
                                   null=True,
                                   blank=True)

    created_at = models.DateTimeField(verbose_name="Дата создания",
                                      auto_now_add=True)

    @property
    def rating(self):
        rating = (Review.objects.filter(title=self).
                  aggregate(Avg('score')).get('score__avg'))
        if rating is None:
            return None
        else:
            return round(rating)

    def __str__(self) -> str:
        return self.description


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name="Текст отзыва"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name='reviews'
    )
    score = models.IntegerField(
        verbose_name="Оценка произведения",
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации отзыва",
        auto_now_add=True
    )

    class Meta:
        unique_together = ['title', 'author']

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='сomments',
    )
    text = models.TextField(
        verbose_name="Текст комментария"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name='сomments'
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации комментария",
        auto_now_add=True
    )

    def __str__(self):
        return self.text
