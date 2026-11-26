from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Concierto, Categoria, TipoBoleto, Compra
from .forms import ConciertoForm, CategoriaForm, TipoBoletoForm

# Verificador de rol Administrador (is_staff o superuser)
def es_admin(user):
    return user.is_authenticated and user.is_staff

def solo_admin(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, "Acceso denegado: No tienes permisos de administrador.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

# --- AUTENTICACIÓN ---
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"¡Bienvenido {user.username}! Tu cuenta ha sido creada.")
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
            if user.is_staff:
                return redirect('dashboard')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'Boletos/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# --- CATÁLOGO PÚBLICO (USUARIOS Y ADMINS) ---
@login_required(login_url='login')
def home_view(request):
    conciertos = Concierto.objects.all().order_by('fecha')
    categorias = Categoria.objects.all()
    return render(request, 'Boletos/home.html', {
        'conciertos': conciertos,
        'categorias': categorias
    })

# --- DASHBOARD ADMINISTRATIVO (SOLO ADMINS) ---
@solo_admin
def dashboard_view(request):
    contexto = {
        'total_conciertos': Concierto.objects.count(),
        'total_categorias': Categoria.objects.count(),
        'total_boletos': TipoBoleto.objects.count(),
        'total_compras': Compra.objects.count(),
        'ultimos_conciertos': Concierto.objects.all().order_by('-id')[:5],
    }
    return render(request, 'Boletos/dashboard.html', contexto)