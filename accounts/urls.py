from django.urls import path
from accounts import views

urlpatterns = [
	path('signup/', views.RegisterView, name="sign-up"),
]