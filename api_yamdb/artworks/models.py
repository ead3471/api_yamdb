from django.db import models
# from django.db.models import Avg

from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User


class Title(models.Model):
    name = models.TextField(verbose_name="Name")
    description = models.TextField(verbose_name="Short description",
                                   null=True,
                                   blank=True)

    created_at = models.DateTimeField(verbose_name="Creation year",
                                      auto_now_add=True)

    # @property
    # def rating(self):
    #     rating = (self.reviews.aggregate(Avg('score')).get('score__avg'))
    #     if rating is None:
    #         return None
    #     else:
    #         return round(rating)

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name="Review text"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Author",
        related_name='reviews'
    )
    score = models.IntegerField(
        verbose_name="Score of the title",
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        verbose_name="Publication date",
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
        verbose_name="Сomment text"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Author",
        related_name='сomments'
    )
    pub_date = models.DateTimeField(
        verbose_name="Publication date",
        auto_now_add=True
    )

    def __str__(self):
        return self.text
