import openpyxl
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from product.models import Product, Tags, Category, Price



class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('amount', 'currency')
        

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('tag_name',)
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category_name',)
        

class ProductSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    category_name = serializers.StringRelatedField()
    price = serializers.StringRelatedField()
    
    class Meta:
        model = Product
        fields = [
            "id",
            "name_of_product",
            "description",
            "price",
            "created_at",
            "category_name",
            "tags"
        ]
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = [tag['tag_name'] for tag in representation['tags']]
        return representation
        
    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        category_data = validated_data.pop('category_name')
        price = validated_data.pop('price')

        tags, _ = Tags.objects.get_or_create(tag_name=tags_data)
        category, _ = Category.objects.get_or_create(category_name=category_data)
        price, _ = Price.objects.get_or_create(amount=price)

        product = Product.objects.create(tags=tags, category_name=category, **validated_data)
        return product
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        category_data = validated_data.pop('category_name', None)
        price_data = validated_data.pop('price', None)

        tags = Tags.objects.get_or_create(tag_name=tags_data) if tags_data is not None else None
        category = Category.objects.get_or_create(category_name=category_data) if category_data is not None else None
        price = Price.objects.get_or_create(amount=price_data) if price_data is not None else None
        
        instance.tags = tags
        instance.category_name = category
        instance.price = price

        instance.save()
        return instance
    
    
class ProductExportView(APIView):
    
    """Здесь скачивается эксель-файл"""
    
    permission_classes = [IsAuthenticated,] #требуется аутентификация

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Products"

        headers = ["ID", "Name", "Description", "Price", "Created At", "Category"]
        ws.append(headers)

        # Заполняем данные
        for product in products:
            row = [
                product.id,
                product.name_of_product,
                product.description,
                str(product.price),
                product.created_at,
                product.category_name.category_name if product.category_name else ""
            ]
            ws.append(row)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=products.xlsx'
        wb.save(response)

        return response