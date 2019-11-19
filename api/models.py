from django.db import models, transaction
from django.db.models import ForeignKey

class Pizza(models.Model):
    SIZE_CHOICES = (
    ('S','small'),
    ('M', 'medium'),
    ('L', 'large'),
    )
    size=models.CharField(max_length=1, choices=SIZE_CHOICES, default="S")
    type = models.CharField(max_length=50, default="Margarita")
    amount = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
            return u'%s / %s / %s' % (self.type, self.size, self.amount)

    def current_count(self):
        return self.amount


class Customer(models.Model):
    name = models.CharField(max_length=80)
    address = models.CharField(max_length=100)

    def __str__(self):
            return u'%s / %s ' % (self.name, self.address)


class Order(models.Model):
    DELIVERED_CHOICES = (
    ('order_getted','ORDER GETTED'),
    ('preparing','PREPARING'),
    ('at_courier', 'AT COURIER',),
    ('delivered','DELIVERED'),
    )
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    delivered = models.CharField(max_length=50, default='order_getted', choices=DELIVERED_CHOICES)

