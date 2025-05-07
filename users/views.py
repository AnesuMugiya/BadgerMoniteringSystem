from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login 
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

def register(request):
     if request.method == 'POST':
          form = UserRegistrationForm(request.POST)
          if form.is_valid():
               form.save()
               user = form.save()
               login(request, user)
               first_name = form.cleaned_data.get('first_name')
               last_name = form.cleaned_data.get('last_name')
               messages.success(request, f'Account created for {first_name} {last_name}!')
               return redirect('dashboard')

     else:
          form = UserRegistrationForm()
     return render(request, 'users/register.html', {'form': form})

@login_required
def account(request):
    return render(request, 'users/account.html')