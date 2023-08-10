from django.db import models


class Price(models.Model):
    CURRENCY_CHOICES = [
        ("KG", "KG"),
        ("USD", "USD"),
        ("EU", "EU"),
        ("RU", "RU"),
    ]    
    amount = models.DecimalField("Стоимость", max_digits=9, decimal_places=2)
    currency = models.CharField("Валюта", max_length=3, choices=CURRENCY_CHOICES, default='KG')
    is_active = models.BooleanField("Актуальна ли?", default=True)
    
    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"
    
    class Meta:
        verbose_name = "Цена"
        verbose_name_plural = "Цены"
        
        
class Tags(models.Model):
    tag_name = models.CharField("Тэг", max_length=100)
    
    def __str__(self) -> str:
        return self.tag_name
        
        
class Category(models.Model):
    category_name = models.CharField("Категория")
    
    def __str__(self) -> str:
        return self.category_name    
            
        
class Product(models.Model):
    name_of_product = models.CharField("Product", max_length=100)
    description = models.CharField("Description", max_length=100)
    created_at = models.DateTimeField("Запись создана", auto_now_add=True)
    updated_at = models.DateTimeField("Запись обновлена", auto_now=True)
    price = models.ForeignKey(Price, related_name="product", on_delete=models.SET_NULL, null=True)
    category_name = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        verbose_name="Категория", 
        related_name="products",
        null=True)
    tags = models.ManyToManyField(Tags)

    
    def __str__(self):
        return self.name_of_product
    
    class Meta:
        ordering = ('name_of_product',)
        verbose_name = "Товар"
        verbose_name_plural = "Товары"    
