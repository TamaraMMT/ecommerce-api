
from rest_framework.routers import DefaultRouter

from product.views import CategoryViewSet, ProductViewSet
from django.urls import path, include


router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"categories", CategoryViewSet, basename='category')

app_name = 'product'

urlpatterns = [
    path('', include(router.urls))
]
