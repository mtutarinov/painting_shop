from django.db import models
from shop.models import Painting
from django.db import transaction
from django.core.exceptions import ValidationError


class Order(models.Model):
    class Status(models.IntegerChoices):
        NOT_PROCESSED = 0, 'Не обработан'
        PROCESSED = 1, 'Обработан'
        SUCCESS = 2, 'Завершен'
        CANCELED = 3, 'Отменен'

    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Почта')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    postal_code = models.CharField(max_length=20, verbose_name='Индекс')
    city = models.CharField(max_length=100, verbose_name='Город')
    status = models.IntegerField(choices=tuple(map(lambda x: (x[0], x[1]), Status.choices)),
                                 default=Status.NOT_PROCESSED, verbose_name="Статус")
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменен')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(painting.get_cost() for painting in self.paintings.all())



class OrderPainting(models.Model):
    order = models.ForeignKey(Order, related_name='order_paintings', on_delete=models.CASCADE, verbose_name='Заказ')
    painting = models.ForeignKey(Painting, related_name='order_paintings', on_delete=models.CASCADE,
                                 verbose_name='Картина')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='Цена')
    class Meta:
        verbose_name = 'Картина в заказе'
        verbose_name_plural = 'Картины в заказе'

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price
