from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Title(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name="Автор",
                               related_name='titles',
                               )

    description = models.TextField(verbose_name="Краткое описание",
                                   null=True,
                                   blank=True)

    rate = models.DecimalField(verbose_name="Рейтинг",
                               max_digits=2,
                               decimal_places=1,
                               default=0)

    created_at = models.DateTimeField(verbose_name="Дата создания",
                                      auto_now_add=True)

    def __str__(self) -> str:
        return self.description
