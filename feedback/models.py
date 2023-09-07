from django.db import models

from user.models import User


# Create your models here.
class Feedback(models.Model):
    text = models.CharField(max_length=255, verbose_name='текст отзыва')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='автор')
    advert = models.ForeignKey(User, on_delete=models.CASCADE, related_name='автор')
    created_at = models.DateTimeField(verbose_name='дата и время создания', auto_now_add=True)

    def __str__(self):
        return f'{self.text}, {self.author}, {self.advert}, {self.created_at}'

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
