from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser): 
    store = models.IntegerField(default=1)
    allowedToReceive = models.BooleanField(default=False)
    allowedToSalesStat = models.BooleanField(default=False)
    owner = models.BooleanField(default = False)