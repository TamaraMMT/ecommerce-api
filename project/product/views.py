from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema
from product.models import (
    Category,
    Product
)
from .serializers import (
    CategorySerializer,
    ProductSerializer,
)


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all categories
    """

    queryset = Category.objects.active()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all products
    """

    queryset = Product.objects.active().prefetch_related(
        Prefetch("product_line__product_image"))

    lookup_field = "slug"

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        """list all products"""
        serializer = ProductSerializer(
            self.queryset,

            many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        """list all products by slug"""
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug)
            .select_related("category"),
            many=True
        )
        return Response(serializer.data)

    @action(
        methods=["get"],
        detail=False,
        url_path=r"category/(?P<slug>[\w-]+)",
    )
    def list_product_by_category_slug(self, request, slug=None):
        """
        An endpoint return products for a specific category
        """
        category = self.queryset.filter(category__slug=slug, category__is_active=True).select_related(
            "category"
        )

        if not category.exists():
            return Response(
                {'error': f'No products found for category: {slug}'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(category, many=True)
        return Response(serializer.data)
