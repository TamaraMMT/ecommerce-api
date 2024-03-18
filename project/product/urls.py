
from rest_framework.routers import DefaultRouter

from product.views import CategoryViewSet, ProductViewSet
from django.urls import path, include


router = DefaultRouter()
router.register(r"", ProductViewSet)

app_name = 'product'

urlpatterns = [
    path('', include(router.urls)),
    path('category', CategoryViewSet.as_view({'get': 'list'})),

]
