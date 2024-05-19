from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null':True}

class Category(models.Model):
    """Категория товара"""


    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    """Продукт"""

    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    preview = models.ImageField(upload_to='catalog/', **NULLABLE, verbose_name='Изображение')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    price = models.PositiveIntegerField(verbose_name='Цена за покупку')
    created_at = models.DateField(auto_now_add=True, **NULLABLE, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, **NULLABLE, verbose_name='Дата последнего изменения')

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)


    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class Blog(models.Model):
    name = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, verbose_name='Ссылка', **NULLABLE)
    content = models.TextField(**NULLABLE, verbose_name='Содержание')
    preview = models.ImageField(upload_to='catalog/', **NULLABLE, verbose_name='Изображение')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, **NULLABLE, verbose_name='Признак публикации')
    views_count = models.IntegerField(**NULLABLE, default=0, verbose_name='Счетчик просмотров')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'


class Version(models.Model):
    """Версия продукта"""
    number = models.PositiveSmallIntegerField(verbose_name='Номер')
    name = models.CharField(max_length=100, verbose_name='Наименование')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    is_active = models.BooleanField(verbose_name='Признак текущей версии')

    def __str__(self):
        return f'{self.number}: {self.name}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'



