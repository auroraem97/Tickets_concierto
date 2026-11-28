"""
URL configuration for tickets_concierto_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tickets_concierto_main.Boletos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # CRUD Conciertos (Wendy)
    path('conciertos/', views.conciertos_list, name='conciertos_list'),
    path('conciertos/crear/', views.concierto_create, name='concierto_create'),
    path('conciertos/editar/<int:pk>/', views.concierto_edit, name='concierto_edit'),
    path('conciertos/eliminar/<int:pk>/', views.concierto_delete, name='concierto_delete'),

    # CRUD Categorías (Vianey)
    path('categorias/', views.categorias_list, name='categorias_list'),
    path('categorias/crear/', views.categoria_create, name='categoria_create'),
    path('categorias/editar/<int:pk>/', views.categoria_edit, name='categoria_edit'),
    path('categorias/eliminar/<int:pk>/', views.categoria_delete, name='categoria_delete'),

    # CRUD Tipos de Boletos (Maia)
    path('boletos/', views.boletos_list, name='boletos_list'),
    path('boletos/crear/', views.boleto_create, name='boleto_create'),
    path('boletos/editar/<int:pk>/', views.boleto_edit, name='boleto_edit'),
    path('boletos/eliminar/<int:pk>/', views.boleto_delete, name='boleto_delete'),
]

