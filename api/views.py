from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from api.serializers import (CustomerSerializer, OrderStatusSerializer,
                             PizzaSerializer, OrderTrackingSerializer,
                             OrderSerializer, OrderUpdateSerializer,AllOrderListSerializer,
                             OrderRemoveSerializer, OrderListSerializer)
from api.models import Customers, Pizzas, Orders
from api.constants import valid_delivered, get_valid_customer_ids


class CustomerCreateView(generics.CreateAPIView):
    serializer_class = CustomerSerializer
    queryset = Customers.objects.all()


class PizzaCreateView(generics.ListCreateAPIView):
    serializer_class = PizzaSerializer
    queryset = Pizzas.objects.all()


class OrderCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Orders.objects.all()


class OrderUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Orders.objects.all()
    lookup_field = 'id'

    def get_object(self):
        return get_object_or_404(Orders, id=self.kwargs['id'])

class OrderRemoveView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderRemoveSerializer
    queryset = Orders.objects.all()
    lookup_field = 'id'

    def get_object(self):
        return get_object_or_404(Orders, id=self.kwargs['id'])


class OrderTrackingView(generics.ListAPIView):
    serializer_class = OrderTrackingSerializer
    queryset = Orders.objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.kwargs['id'])



class OrderStatusUpdateView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Orders.objects.all()
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        return self.queryset.get(id=self.kwargs['id'])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)



class OrderListView(generics.RetrieveAPIView):
    serializer_class = OrderListSerializer
    queryset = Orders.objects.all()

    def get_queryset(self, request, *args, **kwargs):
        order_id = self.request.query_params['order_id']
        return self.queryset.get(id=order_id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset(self, request, *args, **kwargs)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        resp = serializer.save()
        return Response(resp)


class AllOrderListView(generics.ListAPIView):
    serializer_class = AllOrderListSerializer
    queryset = Orders.objects.all()


class SearchOrderView(generics.ListAPIView):
    serializer_class = AllOrderListSerializer
    queryset = Orders.objects.all()

    def get_queryset(self,*args, **kwargs):
        valid_ids = get_valid_customer_ids()
        customer_id = self.request.query_params.get('customer_id', '')
        delivered = self.request.query_params.get('delivered', '')
        if not customer_id and not delivered==False:
            return []
        if int(customer_id) in valid_ids:
            self.queryset.filter(customer_id=int(customer_id))
        if delivered in valid_delivered:
            return self.queryset.filter(delivered=delivered)
        return self.queryset.filter(customer_id=int(customer_id))

