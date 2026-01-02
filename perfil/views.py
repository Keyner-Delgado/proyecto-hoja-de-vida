import os
from django.conf import settings
from django.contrib.staticfiles import finders
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# 1. IMPORTACIÓN ÚNICA DE MODELOS
from .models import (
    DatosPersonales, ExperienciaLaboral, CursosRealizados, 
    Reconocimientos, ProductosAcademicos, ProductosLaborales, 
    VentaGarage, ReporteUnificado
)

# 2. FUNCIÓN DE APOYO PARA EL PDF (Soluciona el Error 500 en Render)
def link_callback(uri, rel):
    """
    Convierte URIs de archivos estáticos y media en rutas absolutas 
    para que xhtml2pdf pueda encontrarlos en el servidor.
    """
    # Si la imagen ya tiene una URL (como las de Cloudinary), pisa la descarga directamente
    if uri.startswith('http'):
        return uri

    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        s_url = settings.STATIC_URL
        s_root = settings.STATIC_ROOT
        m_url = settings.MEDIA_URL
        m_root = settings.MEDIA_ROOT

        if uri.startswith(m_url):
            path = os.path.join(m_root, uri.replace(m_url, ""))
        elif uri.startswith(s_url):
            path = os.path.join(s_root, uri.replace(s_url, ""))
        else:
            return uri

    return path

# 3. VISTAS DEL SITIO WEB
def home(request):
    perfil = DatosPersonales.objects.first()
    return render(request, 'home.html', {'perfil': perfil})

def experiencia(request):
    perfil = DatosPersonales.objects.first()
    items = ExperienciaLaboral.objects.filter(idperfil=perfil)
    return render(request, 'experiencia.html', {'perfil': perfil, 'items': items})

def cursos(request):
    perfil = DatosPersonales.objects.first()
    items = CursosRealizados.objects.filter(idperfil=perfil)
    reporte = ReporteUnificado.objects.filter(tipo='CURSOS').first()
    return render(request, 'cursos.html', {
        'perfil': perfil, 
        'items': items, 
        'reporte_cursos': reporte
    })

def reconocimientos(request):
    perfil = DatosPersonales.objects.first()
    items = Reconocimientos.objects.filter(idperfil=perfil)
    reporte = ReporteUnificado.objects.filter(tipo='RECONOCIMIENTOS').first()
    return render(request, 'reconocimientos.html', {
        'perfil': perfil, 
        'items': items, 
        'reporte_premios': reporte
    })

def productos_academicos(request):
    perfil = DatosPersonales.objects.first()
    items = ProductosAcademicos.objects.filter(idperfil=perfil)
    return render(request, 'productos_academicos.html', {'perfil': perfil, 'items': items})

def productos_laborales(request):
    perfil = DatosPersonales.objects.first()
    items = ProductosLaborales.objects.filter(idperfil=perfil)
    return render(request, 'productos_laborales.html', {'perfil': perfil, 'items': items})

def garage(request):
    perfil = DatosPersonales.objects.first()
    items = VentaGarage.objects.filter(idperfil=perfil)
    return render(request, 'garage.html', {'perfil': perfil, 'items': items})

# 4. VISTA PARA GENERAR EL PDF
def pdf_datos_personales(request):
    # Obtenemos el perfil activo
    perfil = get_object_or_404(DatosPersonales, perfilactivo=1)
    
    # Consultas
    experiencias = ExperienciaLaboral.objects.filter(idperfil=perfil)
    productos_academicos = ProductosAcademicos.objects.filter(idperfil=perfil)
    productos_laborales = ProductosLaborales.objects.filter(idperfil=perfil)
    cursos = CursosRealizados.objects.filter(idperfil=perfil)
    reconocimientos = Reconocimientos.objects.filter(idperfil=perfil)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="CV_{perfil.apellidos}.pdf"'
    
    template = get_template('reportes/pdf_personales.html')
    
    context = {
        'perfil': perfil,
        'items': experiencias,
        'productos': productos_academicos,
        'productos_laborales': productos_laborales,
        'cursos': cursos,
        'reconocimientos': reconocimientos,
    }
    
    html = template.render(context)
    
    # GENERACIÓN DEL PDF CON LINK_CALLBACK
    pisa_status = pisa.CreatePDF(
        html, 
        dest=response, 
        link_callback=link_callback  # <--- Esto es lo que faltaba
    )
    
    if pisa_status.err:
        return HttpResponse('Ocurrió un error al generar el PDF', status=500)
    
    return response