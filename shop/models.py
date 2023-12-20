from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, verbose_name='URL', unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:paintings_by_category', args=(self.slug,))


class Painting(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='paintings', verbose_name='Категория')
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, verbose_name='URL', unique=True)
    image = models.ImageField(upload_to='paintings/%Y/%m/%d',blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2, verbose_name='Цена')
    available = models.BooleanField(default=True, verbose_name='Опубликовано')
    sold = models.BooleanField(default=False, verbose_name='Продано')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменено')

    class Meta:
        ordering = ['-created']
        verbose_name = 'Картина'
        verbose_name_plural = 'Картины'
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:paintings_detail', args=(self.id, self.slug))
