from celery import shared_task
from django.core.cache import cache
from .models import Product

@shared_task
def invalidate_product_list_cache():
    cache.delete('product_list')