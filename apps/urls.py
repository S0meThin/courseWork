from django.urls import path
from . import views

urlpatterns = [
    path('', views.AppsView.default, name = 'defaultApps'),
    path('article_lookup', views.AppsView.artLookup, name='articleLookup'),
    path('inventory_count', views.AppsView.inventoryCount, name = "inventoryCount"),
    path('on_order', views.AppsView.onOrder, name = 'onOrder'),
    path('manual_order', views.AppsView.manualOrder, name = "manualOrder"),
    path('receiving', views.AppsView.receiving, name = "receiving"),
    path('returns', views.AppsView.return_f, name = "returns"),
    path('history_returns', views.AppsView.returns_history, name = "returnsHistory"),
    path('sales_analysis', views.AppsView.salesAnalysis, name ='salesAnalysis'),
    path('orders/<str:order_n>/', views.AppsView.order, name="order"),
    path('item/<str:upc>/', views.AppsView.item, name="itemInfo"),
    path('orderInfo/<str:order_n>/', views.AppsView.orderInfo, name='orderInfo'),
]
