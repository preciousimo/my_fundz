from django.urls import path
from userauth import views

app_name = "userauth"

urlpatterns = [
    path("", views.account, name="account"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("kyc-reg/", views.kyc_registration, name="kyc-reg"),
    path('change-pin/', views.change_pin, name='change-pin'),
]