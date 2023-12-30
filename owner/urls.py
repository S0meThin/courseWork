from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainPage, name='mainPage'),
    path('sales', views.sales, name = "sales"),
    path('salesInfo/<str:store>', views.salesInfo, name = "salesInfo"),
    path('returns', views.returnsO, name = "returns"),
    path('returnsInfo/<str:store>', views.returnsInfo, name = "returnsInfo"),
    path('items', views.items, name = "items"),
    path('itemsInfo/<str:store>/<str:item>', views.itemsInfo, name = "itemsInfo")
]
