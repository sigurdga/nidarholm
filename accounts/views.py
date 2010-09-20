from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect('/')
    else:
        form = AuthenticationForm(request)

    return render_to_response("accounts/login.html", {'form': form})

def logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                    username=form.cleaned_data.get("username"),
                    password=form.cleaned_data.get("password1"))
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    return render_to_response("accounts/register.html", {'form': form})