from django.db import models

from advert.models import Advert
from user.models import User


# Модель для отзыва с полями по тз.
class Feedback(models.Model):
    text = models.CharField(
        max_length=255,
        verbose_name='текст отзыва'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='пользователь'
    )
    advert = models.ForeignKey(
        Advert,
        on_delete=models.CASCADE,
        related_name='объявление'
    )
    created_at = models.DateTimeField(
        verbose_name='дата и время создания',
        auto_now_add=True
    )

    def __str__(self):
        return (f'{self.text}, {self.user}, '
                f'{self.advert}, {self.created_at}')

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
