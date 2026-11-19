from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

def __str__(self):
    return self.nombre

class Concierto(models.Model):
    nombre = models.CharField(max_length=200)
    artista = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    lugar = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='conciertos/',blank=True, null=True)
    descripcion = models.TextField()

def __str__(self):
    return f"{self.nombre} - {self.artista}"

class TipoBoleto(models.Model):
    concierto = models.ForeignKey(Concierto,on_delete=models.CASCADE,related_name='boletos')
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.IntegerField()
    beneficios = models.TextField(blank=True)

def __str__(self):
    return f"{self.concierto.nombre} - {self.nombre}"

class Compra(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    boleto = models.ForeignKey(TipoBoleto,on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    total = models.DecimalField(max_digits=10,decimal_places=2)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    codigo = models.CharField(max_length=20,unique=True)

def __str__(self):
    return f"Compra {self.codigo} - {self.usuario.username}"