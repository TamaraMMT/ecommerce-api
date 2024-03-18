from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import action
from product.models import (
    Category,
    Product,
    ProductLine
)
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductlineSerializer
)


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
    lookup_field = "slug"

    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug), many=True
        )
        return Response(serializer.data)

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["get"],
        detail=False,
        url_path=r"category/(?P<name>[\w-]+)",
    )
    def list_product_by_category_name(self, request, name=None):
        """
        An endpoint to return products by category
        """
        filtered_products = self.queryset.filter(category__name=name)

        if not filtered_products.exists():
            return Response(
                {'error': f'No products found for category: {name}'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(filtered_products, many=True)
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
