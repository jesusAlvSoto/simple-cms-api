from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserList.as_view()),
    path('<pk>/', views.UserDetail.as_view()),
]