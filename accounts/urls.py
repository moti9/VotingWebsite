from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.create_user, name='register'),
    path('send/', views.send_verification_code, name='send_verification_code'),
    path('verify/', views.verify_email, name='verify_email'),
]
