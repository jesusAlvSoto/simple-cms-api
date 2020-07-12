from .serializers import CustomerSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from .models import Customer


class CustomerList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
