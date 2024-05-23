from catalog.models import Category
from django.core.cache import cache
from config.settings import CACHE_ENABLED

def get_cashed_category_list():
    """Функция возвращает закешированный список категорий"""

    if not CACHE_ENABLED:
        category_list = Category.objects.all()
        return category_list
    key = 'categories'
    category_list = cache.get(key)
    if category_list is not None:
        return category_list
    category_list = Category.objects.all()
    cache.set(key, category_list)
    return category_list