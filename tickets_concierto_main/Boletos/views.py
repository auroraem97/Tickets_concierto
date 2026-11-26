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

# --- CRUD DE CONCIERTOS (WENDY) ---
@solo_admin
def conciertos_list(request):
    conciertos = Concierto.objects.all().order_by('-fecha')
    return render(request, 'Boletos/conciertos_list.html', {'conciertos': conciertos})

@solo_admin
def concierto_create(request):
    if request.method == 'POST':
        form = ConciertoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Concierto registrado exitosamente!")
            return redirect('conciertos_list')
    else:
        form = ConciertoForm()
    return render(request, 'Boletos/concierto_form.html', {'form': form, 'titulo': 'Registrar Nuevo Concierto'})

@solo_admin
def concierto_edit(request, pk):
    concierto = get_object_or_404(Concierto, pk=pk)
    if request.method == 'POST':
        form = ConciertoForm(request.POST, instance=concierto)
        if form.is_valid():
            form.save()
            messages.success(request, f"El concierto '{concierto.nombre}' fue actualizado.")
            return redirect('conciertos_list')
    else:
        form = ConciertoForm(instance=concierto)
    return render(request, 'Boletos/concierto_form.html', {'form': form, 'titulo': f'Editar Concierto: {concierto.nombre}'})

@solo_admin
def concierto_delete(request, pk):
    concierto = get_object_or_404(Concierto, pk=pk)
    if request.method == 'POST':
        nombre = concierto.nombre
        concierto.delete()
        messages.warning(request, f"Concierto '{nombre}' eliminado correctamente.")
        return redirect('conciertos_list')
        return render (request, 'Boletos/concierto_confirm_delete.html',{'concierto': concierto})

# --- CRUD DE CATEGORÍAS (VIANEY) ---
@solo_admin
def categorias_list(request):
    categorias = Categoria.objects.all().order_by('nombre')
    return render(request, 'Boletos/categorias_list.html', {'categorias': categorias})

@solo_admin
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Categoría creada exitosamente!")
            return redirect('categorias_list')
    else:
        form = CategoriaForm()
    return render(request, 'Boletos/categoria_form.html', {'form': form, 'titulo': 'Nueva Categoría Musical'})

@solo_admin
def categoria_edit(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, f"Categoría '{categoria.nombre}' actualizada.")
            return redirect('categorias_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'Boletos/categoria_form.html', {'form': form, 'titulo': f'Editar Categoría: {categoria.nombre}'})

@solo_admin
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        nombre = categoria.nombre
        categoria.delete()
        messages.warning(request, f"Categoría '{nombre}' eliminada.")
        return redirect('categorias_list')
    return render(request, 'Boletos/categoria_confirm_delete.html', {'categoria': categoria})

# --- CRUD DE TIPOS DE BOLETOS (MAIA) ---
@solo_admin
def boletos_list(request):
    boletos = TipoBoleto.objects.select_related('concierto').all().order_by('concierto__nombre', 'precio')
    return render(request, 'Boletos/boletos_list.html', {'boletos': boletos})

@solo_admin
def boleto_create(request):
    if request.method == 'POST':
        form = TipoBoletoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tipo de boleto registrado exitosamente!")
            return redirect('boletos_list')
    else:
        form = TipoBoletoForm()
    return render(request, 'Boletos/boleto_form.html', {'form': form, 'titulo': 'Nuevo Tipo de Boleto'})

@solo_admin
def boleto_edit(request, pk):
    boleto = get_object_or_404(TipoBoleto, pk=pk)
    if request.method == 'POST':
        form = TipoBoletoForm(request.POST, instance=boleto)
        if form.is_valid():
            form.save()
            messages.success(request, f"Boleto '{boleto.nombre}' actualizado correctamente.")
            return redirect('boletos_list')
    else:
        form = TipoBoletoForm(instance=boleto)
    return render(request, 'Boletos/boleto_form.html', {'form': form, 'titulo': f'Editar Boleto: {boleto.nombre}'})

@solo_admin
def boleto_delete(request, pk):
    boleto = get_object_or_404(TipoBoleto, pk=pk)
    if request.method == 'POST':
        nombre = boleto.nombre
        boleto.delete()
        messages.warning(request, f"Tipo de boleto '{nombre}' eliminado.")
        return redirect('boletos_list')
    return render(request, 'Boletos/boleto_confirm_delete.html', {'boleto': boleto})