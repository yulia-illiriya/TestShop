from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.views import ProductExportView



urlpatterns = [
    path('export/', ProductExportView.as_view(), name='products_export'),
]