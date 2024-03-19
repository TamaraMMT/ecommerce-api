from rest_framework.routers import DefaultRouter

from product.views import CategoryViewSet, ProductViewSet
from django.urls import path, include


router = DefaultRouter()
router.register(r"products", ProductViewSet)  # Registro de las vistas de productos bajo el endpoint "products"
router.register(r"categories", CategoryViewSet)  # Registro de las vistas de categorías bajo el endpoint "categories"

app_name = 'product'

urlpatterns = [
    path('', include(router.urls)),  # Incluye las URLs generadas por el enrutador
]