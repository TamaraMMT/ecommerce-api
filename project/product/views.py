from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response

from product.models import Category, Product, ProductLine
from .serializers import CategorySerializer, ProductSerializer, ProductlineSerializer


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all categories
    """

    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all products
    """

    queryset = Product.objects.all()

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductlineViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all productsline
    """

    queryset = ProductLine.objects.all()

    @extend_schema(responses=ProductlineSerializer)
    def list(self, request):
        serializer = ProductlineSerializer(self.queryset, many=True)
        return Response(serializer.data)

