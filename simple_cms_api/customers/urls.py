from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.CustomerList.as_view(), name='customers-list'),
    path('<pk>/', views.CustomerDetail.as_view(), name='customer-detail'),
]