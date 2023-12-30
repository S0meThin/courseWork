from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainMenu, name='mainMenu'),
    path('order_management', views.orderManagement, name='orderManagement'),
]
