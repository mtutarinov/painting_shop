# Generated by Django 5.0 on 2023-12-12 07:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['name'],
                'indexes': [models.Index(fields=['name'], name='shop_catego_name_289c7e_idx')],
            },
        ),
        migrations.CreateModel(
            name='Painting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='URL')),
                ('image', models.ImageField(blank=True, upload_to='paintings/%Y/%m/%d', verbose_name='Изображение')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('available', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Изменено')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paintings', to='shop.category', verbose_name='Категория')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]