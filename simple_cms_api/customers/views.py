from .serializers import CustomerSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Customer


class CustomerList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
