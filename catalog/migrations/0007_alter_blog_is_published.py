# Generated by Django 5.0.3 on 2024-04-24 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='is_published',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Признак публикации'),
        ),
    ]