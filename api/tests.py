from django.test import TestCase
from api.models import Customer, Pizza, Order

class ModelTestCase(TestCase):


    def setUp(self):
        self.pizza_type = "Margarita"
        self.pizza_size='S'
        self.pizza_amount = 150
        self.pizza = Pizza(type=self.pizza_type, size=self.pizza_size, amount=self.pizza_amount)
        self.pizza.save()

        self.customer_name = "testname"
        self.customer_address = "testaddress"
        self.customer = Customer(name = self.customer_name, address = self.customer_address)
        self.customer.save()

        self.order = Order(customer=self.customer, pizza=self.pizza, quantity=5)

    def test_create_order(self):
        before= Order.objects.all().count()
        self.order.save()
        after= Order.objects.all().count()
        self.assertNotEqual(before, after)


