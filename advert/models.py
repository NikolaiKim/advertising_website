from django.db import models

from user.models import User


# Create your models here.
class Advert(models.Model):
    title = models.CharField(max_length=255, verbose_name='название')
    price = models.IntegerField(verbose_name='цена')
    description = models.CharField(max_length=255, verbose_name='название')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='автор')
    created_at = models.DateTimeField(verbose_name='дата и время создания', auto_now_add=True)

    def __str__(self):
        return f'{self.title}, {self.price}, {self.description}, {self.author}, {self.created_at}'

    class Meta:
        verbose_name = 'объявление'
        verbose_name_plural = 'объявления'
