from django.contrib import admin
from django.urls import path
from App import views
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('register',views.register,name='register'),
    path('verify',views.verify,name="verify"),
    path('send_otp',views.send_otp,name="send_otp"),
    path('profile',views.profile,name='profile'),
    path('logout',views.logout,name='logout'),
    path('delete',views.delete,name="delete"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="forget-password.html"), name="reset_password"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_email.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset-password.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_complete.html"), name='password_reset_complete')
   
]
