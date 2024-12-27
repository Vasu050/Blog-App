from django.contrib import admin
from django.urls import path
from App import views
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('register',views.register,name='register'),
    # path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    #path('forgot-password/', views.forgot_password_view, name='forgot-password'),
    #path('reset-password/<str:token>/', views.reset_password_view, name='reset-password'),


    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="forget-password.html"), name="reset_password"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_email.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset-password.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_complete.html"), name='password_reset_complete'),
]
