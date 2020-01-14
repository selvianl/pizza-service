from rest_framework import serializers
from api.models import Pizza, Customer, Order
from django.db import models, transaction, OperationalError


class PizzaSerializer(serializers.ModelSerializer):

    def save(self):
        data = self.validated_data
        # if attemps to add with same name and size
        if Pizza.objects.filter(type=data['type'], size=data['size']).exists():
            return Pizza.objects.filter(type=data['type'], size=data['size']).update(amount=data['amount'])
        return Pizza.objects.create(type=data['type'], size=data['size'], amount=data['amount'])


    class Meta:
        model=Pizza
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model=Customer
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    pizza= PizzaSerializer(many=True, read_only=True)
    customer= CustomerSerializer(many=True, read_only=True)

    def create(self, validated_data):
        import ipdb
        ipdb.set_trace()

    class Meta:
        model=Order
        fields = ('pizza', 'customer', 'quantity')


#    def validate(self,data):
#        # order the same flavor of pizza but with different sizes
#        if Order.objects.filter(customer=data['customer'].id, pizza=data['pizza'].id).exists():
#            raise serializers.ValidationError("This user has already order.")
#        return data

#    def save(self):
#        pizza_id = self.validated_data['pizza']
#        customer_id = self.validated_data['customer']
#        quantity = self.validated_data['quantity']
#        customer = Customer.objects.get(id=customer_id.id)
#        pizza = Pizza.objects.get(id=pizza_id.id)

        # lock database for same time orders
##        with transaction.atomic():
#            pizza_amount = Pizza.objects.select_for_update(nowait=True).get(id=pizza.id).amount
#            if not pizza_amount >= quantity:
#                raise('There is not enough ' + pizza.type + " or it has been deposit for someone.")
#
#            # create order
#            order = Order.objects.create(pizza=pizza, customer=customer_id,
#                                         quantity=quantity, delivered='order_getted')
#            pizza_amount -= quantity
#            order.save()
#
#        # updating pizza amount
#        Pizza.objects.filter(size=pizza.size,
#                             type=pizza.type).update(amount=pizza_amount)
#
#        resp = {
#            "order_id": pizza.id,
#            "customer" : customer.name,
#            "address" : customer.address,
#            "pizza" : pizza.type,
#            "size" : pizza.size,
#            "quantity" : quantity,
#        }
#
#        return resp

class OrderUpdateSerializer(serializers.ModelSerializer):

    def validate(self, attr):
        current_order_id = self.context['view'].kwargs.get('id')
        is_delivered = Order.objects.get(id=current_order_id).delivered

        # order can be updated before giving to courier
        if is_delivered != 'order_getted' and is_delivered !='preparing':
            raise serializers.ValidationError("It is too late to update order..")

        quantity= attr['quantity']
        incoming_order = attr['pizza']
        current_order = self.instance.pizza
        current_order_quantity = Order.objects.get(id=current_order_id).quantity


        # If everthing is same just pass without caring amount
        if incoming_order.type == current_order.type \
            and incoming_order.size==current_order.size \
            and quantity == current_order_quantity:
            return attr

        # Updating amount of incoming pizza type
        Pizza.objects.filter(size=incoming_order.size,
                             type=incoming_order.type).update(amount=
                                                     incoming_order.current_count()
                                                     -quantity)

        # Updating amount of changed pizza type
        Pizza.objects.filter(size=current_order.size,
                             type=current_order.type).update(
                             amount=current_order.current_count()+current_order_quantity)
        return attr

    class Meta:
        model=Order
        fields=('customer', 'pizza', 'quantity')


class OrderStatusSerializer(serializers.ModelSerializer):

    def validate_delivered(self, attrs):
        status = attrs
        current_status = self.instance.delivered
        if not current_status == 'delivered':
            return status
        raise serializers.ValidationError('This pizza has already sent or on way')

    class Meta:
        model=Order
        exclude = ('pizza', 'customer', 'quantity')


class OrderTrackingSerializer(serializers.ModelSerializer):

    class Meta:
        model=Order
        exclude = ('pizza', 'customer', 'quantity')








class OrderRemoveSerializer(serializers.ModelSerializer):

    class Meta:
        model=Order
        fields = ('delivered', 'pizza', 'customer')


class OrderListSerializer(serializers.ModelSerializer):

    def save(self):
        resp = {}
        resp['id'] = self.instance.id
        resp['customer'] = self.instance.customer.name
        resp['address'] = self.instance.customer.address
        resp['pizza'] = self.instance.pizza.type
        resp['quantity'] = self.instance.quantity
        resp['delivered'] = self.instance.delivered
        return resp

    class Meta:
        model=Order
        fields ="__all__"
        read_only_fields = ['pizza', 'customer', 'quantity', 'delivered']


class AllOrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields ="__all__"
