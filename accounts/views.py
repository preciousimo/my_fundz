from django.shortcuts import render, redirect
from accounts.forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def RegisterView(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect('/')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=True)
            username = form.cleaned_data['username']
            messages.success(request, f"New Account Created: {username}.")
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('/')
    else:
        form =  UserRegisterForm()

    context = {'form': form}
    return render(request, "accounts/sign_up.html", context)
