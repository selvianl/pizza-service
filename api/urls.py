from django.conf.urls import url, include
from api import views

urlpatterns = [
    url(r'^create_customer/$', views.CustomerCreateView.as_view(), name='user_create' ),
    url(r'^pizzas/$', views.PizzaCreateView.as_view(), name='pizza_create' ),
    url(r'^orders/$', views.OrderCreateView.as_view(), name='order_create' ),
    url(r'^orders/(?P<id>[0-9]+)/$', views.OrderUpdateView.as_view(), name='detail_order'),
    url(r'^track_status_order/(?P<id>[0-9]+)/$', views.OrderTrackingView.as_view(), name='tracking_order'),
    url(r'^update_status_order/(?P<id>[0-9]+)/$', views.OrderStatusUpdateView.as_view(), name='status_order'),
    url(r'^remove_order/(?P<id>[0-9]+)/$', views.OrderRemoveView.as_view(), name='remove_order'),
    url(r'^detail_order/$', views.OrderListView.as_view(), name='detail_order'),
    url(r'^list_order/$', views.AllOrderListView.as_view(), name='all_order_list'),
    url(r'^search_order/$', views.SearchOrderView.as_view(), name='search_order'),
]
