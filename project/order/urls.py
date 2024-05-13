"""
URL mappings for the order API.
"""

from order import views
from django.urls import path


app_name = 'order'


urlpatterns = [
    path('items/', views.OrderItemView.as_view(), name='items'),
]
