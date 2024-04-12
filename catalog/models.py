from django.db import models

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


    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
