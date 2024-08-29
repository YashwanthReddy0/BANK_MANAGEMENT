from django.urls import path
from . import views

urlpatterns = [
    path('', views.details, name='1'),
    path('details/', views.details, name='bankdetails'),
    path('validate/', views.validate_pin, name='validate_pin'),
    path('withdraw/<int:pk>/', views.withdraw, name='withdraw'),
    path('deposit/<int:pk>/', views.deposit, name='deposit'),
    path('transfer/<int:pk>/', views.transfer, name='transfer'),
    path('forgot_pin/', views.forgot_pin, name='forgot_pin'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('reset_pin/<int:pk>/', views.reset_pin, name='reset_pin'),
    path('forgot_account_number/', views.forgot_account_number, name='forgot_account_number'),
    path('transaction_history/<int:pk>/', views.transaction_history, name='transaction_history'),  # Add this line
]
