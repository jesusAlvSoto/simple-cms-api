from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('customers/', include('customers.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
