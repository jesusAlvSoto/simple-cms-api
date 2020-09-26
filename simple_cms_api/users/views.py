from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

class UserList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser, TokenHasReadWriteScope]
    queryset = get_user_model().objects.filter(is_active=True)
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser, TokenHasReadWriteScope]
    queryset = get_user_model().objects.filter(is_active=True)
    serializer_class = UserSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=['is_active'])