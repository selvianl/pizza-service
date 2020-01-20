from api.models import Customers

valid_delivered = ['order_getted', 'preparing', 'at_courier', 'delivered']

def get_valid_customer_ids():
    valid_customer_id = []
    objects = Customers.objects.all()
    for obj in objects:
        if obj.id not in valid_customer_id:
            valid_customer_id.append(obj.id)
    return valid_customer_id




