from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
@login_required
def profile(request):
    return render(request,'profile.html')

def registration(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    else:
        form = RegisterForm()
    return render(response,"register.html",{"form":form})
