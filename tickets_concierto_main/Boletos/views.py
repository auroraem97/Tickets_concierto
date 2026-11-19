from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Concierto, Categoria

def register_view(request):
    if request.method == 'POST':
       form = UserCreationForm(request.POST)
       if form.is_valid():
          user = form.save()
          login(request, user)
          return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'Boletos/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
       form = AuthenticationForm(data=request.POST)
       if form.is_valid():
          user = form.get_user()
          login(request, user)
          return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'Boletos/login.html',{'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home_view(request):
    conciertos = Concierto.objects.all().order_by('fecha')
    categorias = Categoria.objects.all()
    return render(request, 'Boletos/home.html', {'conciertos': conciertos,'categorias': categorias
})