from rest_framework import serializers
from api.models import Pizzas, Customers, Orders
from django.db import models, transaction, OperationalError


class PizzaSerializer(serializers.ModelSerializer):

#    def save(self):
#        data = self.validated_data
#        # if attemps to add with same name and size
#        if Pizza.objects.filter(type=data['type'], size=data['size']).exists():
#            return Pizza.objects.filter(type=data['type'], size=data['size']).update(amount=data['amount'])
 #       return Pizza.objects.create(type=data['type'], size=data['size'], amount=data['amount'])

    class Meta:
        model=Pizzas
        fields = ('size', 'type')


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model=Customers
        fields = ('name', 'address')


class OrderSerializer(serializers.ModelSerializer):
    pizza= PizzaSerializer(many=True, read_only=True)
    customer= CustomerSerializer(many=True, read_only=True)

    def validate(self,data):
        data['pizza'] = []
        data['customer'] = []
        if 'pizza' in self.initial_data:
            pizzas = self.initial_data.pop('pizza')
            for pizza in pizzas:
                if not Pizzas.objects.filter(**pizza).exists():
                    raise serializers.ValidationError("Pizza is not exists")
                pizza_obj = Pizzas.objects.get(**pizza)
                if data['pizza']:
                    for exist_pizza in data['pizza']:
                        if exist_pizza.id == pizza_obj.id:
                            raise serializers.ValidationError("You can select same type pizza but different sizes.")
                data['pizza'].append(pizza_obj)

        if 'customer' in self.initial_data:
            customers = self.initial_data.pop('customer')
            for customer in customers:
                if not Customers.objects.filter(**customer).exists():
                    raise serializers.ValidationError("Customer is not exists")
                customer_obj = Customers.objects.get(**customer)
                data['customer'].append(customer_obj)
        return data


        # order the same flavor of pizza but with different sizes
        #if Order.objects.filter(customer=data['customer'].id, pizza=data['pizza'].id).exists():
        #    raise serializers.ValidationError("This user has already order.")

    def create(self, validated_data):
        amount = validated_data.pop('amount')
        order = Orders.objects.create(amount=amount)
        for pizza in validated_data.pop('pizza'):
            order.pizza.add(pizza)
            order.save()
        for customer in validated_data.pop('customer'):
            order.customer.add(customer)
            order.save()
        return order


    def update(self, instance, validated_data):
        pizzas =  validated_data['pizza']
        customers =  validated_data['customer']
        for pizza in pizzas:
            instance.pizza.clear()
            instance.pizza.add(pizza)
        for customer in customers:
            instance.customer.clear()
            instance.customer.add(customer)
        instance.save()
        return instance


    class Meta:
        model=Orders
        fields = ('pizza', 'customer', 'amount')




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
        model=Orders
        fields=('customer', 'pizza', 'quantity')


class OrderStatusSerializer(serializers.ModelSerializer):

    def validate_delivered(self, attrs):
        status = attrs
        current_status = self.instance.delivered
        if not current_status == 'delivered':
            return status
        raise serializers.ValidationError('This pizza has already sent or on way')

    class Meta:
        model=Orders
        exclude = ('pizza', 'customer', 'quantity')


class OrderTrackingSerializer(serializers.ModelSerializer):

    class Meta:
        model=Orders
        exclude = ('pizza', 'customer', 'quantity')








class OrderRemoveSerializer(serializers.ModelSerializer):

    class Meta:
        model=Orders
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
        model=Orders
        fields ="__all__"
        read_only_fields = ['pizza', 'customer', 'quantity', 'delivered']


class AllOrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Orders
        fields ="__all__"
