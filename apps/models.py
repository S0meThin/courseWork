from django.db import models

class Store(models.Model):
    number = models.IntegerField(default = 1)

class itemList(models.Model): 
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    UPC = models.CharField(max_length = 12)
    name = models.CharField(max_length = 20)
    oh = models.IntegerField()
    pack = models.IntegerField()
    price = models.FloatField(default = 0)
    retail = models.FloatField(default = -1)

class orders(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    delN = models.CharField(max_length = 9, unique = True)
    dateO = models.DateField()
    dateD = models.DateField(default = '2004-12-12')
    status = models.BooleanField(default = False)

class itemOrdered(models.Model):
    order = models.ForeignKey(orders, on_delete=models.CASCADE)
    item = models.ForeignKey(itemList, on_delete = models.CASCADE)
    qty = models.IntegerField()

class transactions(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    item = models.ForeignKey(itemList, on_delete = models.CASCADE)
    type = models.CharField(max_length = 50)
    qty = models.IntegerField() 
    timeTr = models.DateField(default = '2004-12-12')

class returns(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    item = models.ForeignKey(itemList, on_delete = models.CASCADE)
    dateR = models.DateField()
    qty = models.IntegerField()
    user = models.CharField(max_length = 50)
    status = models.BooleanField(default = False)