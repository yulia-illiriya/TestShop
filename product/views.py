import openpyxl

from django.shortcuts import render
from django.core.cache import cache
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):    
    queryset = Product.objects.select_related('category_name', 'price').prefetch_related('tags')
    serializer_class = ProductSerializer
    
    def get(self, request, *args, **kwargs):
        cache_key = 'product_list'
        products = cache.get(cache_key)

        if products is None:
            products = Product.objects.select_related('category_name', 'price').prefetch_related('tags').all()
            cache.set(cache_key, products, timeout=60 * 15)  # Кешируем на 15 минут

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


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