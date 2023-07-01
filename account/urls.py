from django.urls import path, include
from account.views import UserRegisterationView
urlpatterns = [
    path('register/', UserRegisterationView.as_view(),name='register'),
   
]