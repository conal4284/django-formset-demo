from django.urls import path

from order.views import OrderCreate, OrderUpdate, OrderList


urlpatterns = [
    path('order/add/', OrderCreate.as_view(), name='add_order'),
    path('<pk>/order/update/', OrderUpdate.as_view(), name='update_order'),
    path('order/list/', OrderList.as_view(), name='list_order'),
]