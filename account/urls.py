from django.urls import path, include
from account.views import UserRegisterationView,UserLoginView,UserProfileView, UserChangePasswordView, SendPasswordResetEmailView, UserPasswordResetView, UserLogoutView
urlpatterns = [
    path('register/', UserRegisterationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('profile/', UserProfileView.as_view(),name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(),name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(),name='send_password_reset_email'),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name='password_reset'),
    path('logout/',UserLogoutView.as_view(),name='logout')
]