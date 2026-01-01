from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('experiencia/', views.experiencia, name='experiencia'),
    path('cursos/', views.cursos, name='cursos'),
    path('reconocimientos/', views.reconocimientos, name='reconocimientos'),
    path('productos-academicos/', views.productos_academicos, name='productos_academicos'),
    # Nueva ruta:
    path('productos-laborales/', views.productos_laborales, name='productos_laborales'),
    path('garage/', views.garage, name='garage'),
    path('reporte-personal/', views.pdf_datos_personales, name='pdf_personales'),
]

