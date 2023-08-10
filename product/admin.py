from django.contrib import admin

from .models import Price, Product, Category, Tags

admin.site.register(Product)
admin.site.register(Price)
admin.site.register(Category)
admin.site.register(Tags)
