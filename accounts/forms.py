from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User

# Define a constant for the input class
INPUT_CLASS = "form-control rounded-input"

class UserRegisterForm(UserCreationForm):
	username = forms.CharField(label='Username', widget=forms.TextInput(attrs={"class": INPUT_CLASS, 'placeholder':'Username'}))
	email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={"class": INPUT_CLASS, 'placeholder':'Email'})) 
	password1 = forms.CharField(label='Enter Password', widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, 'placeholder':'Password'}))
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={"class": INPUT_CLASS, 'placeholder':'Confirm Password'}))
	
	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]