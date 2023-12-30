from django.contrib import admin
from .models import itemList, orders, itemOrdered, transactions, returns, Store

# Register your models here.

admin.site.register(itemList)
admin.site.register(orders)
admin.site.register(itemOrdered)
admin.site.register(transactions)
admin.site.register(returns)
admin.site.register(Store)
