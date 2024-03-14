
from rest_framework.routers import DefaultRouter

from product.views import CategoryViewSet, ProductViewSet, ProductlineViewSet
from django.urls import path, include


router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"categories", CategoryViewSet, basename='category')
router.register(r"productline", ProductlineViewSet)

app_name = 'product'

urlpatterns = [
    path('', include(router.urls))
]
