from django.db import models, transaction
from django.db.models import ForeignKey

class Pizzas(models.Model):
    SIZE_CHOICES = (
    ('S','small'),
    ('M', 'medium'),
    ('L', 'large'),
    )
    size=models.CharField(max_length=1, choices=SIZE_CHOICES, default="S")
    type = models.CharField(max_length=50, default="Margarita")

    def __str__(self):
        return u'%s / %s ' % (self.type, self.size)


class Customers(models.Model):
    name = models.CharField(max_length=80)
    address = models.CharField(max_length=100)

    def __str__(self):
            return u'%s / %s ' % (self.name, self.address)


class Orders(models.Model):
    DELIVERED_CHOICES = (
    ('order_getted','ORDER GETTED'),
    ('preparing','PREPARING'),
    ('at_courier', 'AT COURIER',),
    ('delivered','DELIVERED'),
    )
    amount = models.PositiveIntegerField()
    pizza = models.ManyToManyField(Pizzas)
    customer = models.ManyToManyField(Customers)
    delivered = models.CharField(max_length=50, default='order_getted', choices=DELIVERED_CHOICES)

