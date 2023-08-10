from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from .tasks import invalidate_product_list_cache
from .models import Product

@receiver(post_save, sender=Product)
def invalidate_product_list_cache(sender, instance, **kwargs):
    invalidate_product_list_cache.delay()
    