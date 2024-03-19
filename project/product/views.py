from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import action
from product.models import (
    Category,
    Product,
)
from .serializers import (
    CategorySerializer,
    ProductSerializer,
)


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all categories
    """

    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        queryset = self.queryset.filter(is_active=True)
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all products
    """

    queryset = Product.objects.filter(is_active=True)
    
    lookup_field = "slug"

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug), many=True
        )
        return Response(serializer.data)

    @action(
        methods=["get"],
        detail=False,
        url_path=r"category/(?P<slug>[\w-]+)",
    )
    def list_product_by_category_slug(self, request, slug=None):
        """
        An endpoint to return products by category
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

'''
class ProductlineViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all productsline
    """

    queryset = ProductLine.objects.all()

    @extend_schema(responses=ProductlineSerializer)
    def list(self, request):
        serializer = ProductlineSerializer(self.queryset, many=True)
        return Response(serializer.data)
        '''