from django.urls import path
from accounts import views

urlpatterns = [
	path('signup/', views.RegisterView, name="signup"),
	path('login/', views.LoginView, name="login"),
	path('logout/', views.LogoutView, name="logout"),
]