from functools import total_ordering
from operator import itemgetter
from django.db import models

# Create your models here.
class Order(models.Model):
    customer_name = models.CharField(max_length=50, null=True, blank=False)
    customer_address = models.CharField(max_length=50, null=True, blank=True)
    customer_phone = models.CharField(max_length=50, null=True, blank=True)

class OrderParticulars(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    item_name =models.CharField(max_length=50, null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.CharField(max_length=50, null=True, blank=True)
    total = models.CharField(max_length=50, null=True, blank=True)

