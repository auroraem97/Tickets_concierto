from django import forms
from .models import Concierto, Categoria, TipoBoleto

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Pop, Urbano, Regional'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del género...'}),
        }

class ConciertoForm(forms.ModelForm):
    class Meta:
        model = Concierto
        fields = ['nombre', 'artista', 'categoria', 'fecha', 'lugar', 'ciudad', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del tour o evento'}),
            'artista': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del artista o banda'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'lugar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Estadio GNP Seguros'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. CDMX, Tijuana'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TipoBoletoForm(forms.ModelForm):
    class Meta:
        model = TipoBoleto
        fields = ['concierto', 'nombre', 'precio', 'stock', 'beneficios']
        widgets = {
            'concierto': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. VIP, General, Platino'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '1'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'beneficios': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ej. Acceso anticipado, bebida incluida'}),
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio del boleto debe ser mayor a $0.")
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError("El stock no puede ser un número negativo.")
        return stock