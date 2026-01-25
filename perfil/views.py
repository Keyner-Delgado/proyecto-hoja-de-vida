import os
import io
import requests
from django.conf import settings
from django.contrib.staticfiles import finders
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# NUEVAS IMPORTACIONES PARA UNIR PDFs
from pypdf import PdfWriter 
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# 1. IMPORTACIÓN DE MODELOS
from .models import (
    DatosPersonales, ExperienciaLaboral, CursosRealizados, 
    Reconocimientos, ProductosAcademicos, ProductosLaborales, 
    VentaGarage
)

# 2. FUNCIONES DE APOYO (Helpers)
def link_callback(uri, rel):
    """Convierte URIs de archivos estáticos y media en rutas absolutas."""
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

def crear_caratula(texto):
    """Crea una página PDF con un título grande para separar secciones."""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica-Bold", 32)
    can.drawCentredString(300, 500, texto.upper())
    can.save()
    packet.seek(0)
    return packet

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
    return render(request, 'cursos.html', {'perfil': perfil, 'items': items})

def reconocimientos(request):
    perfil = DatosPersonales.objects.first()
    items = Reconocimientos.objects.filter(idperfil=perfil)
    return render(request, 'reconocimientos.html', {'perfil': perfil, 'items': items})

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

# 4. VISTA MAESTRA PARA GENERAR EL PDF
def pdf_datos_personales(request):
    perfil = get_object_or_404(DatosPersonales, perfilactivo=1)
    
    # CAPTURA DE PARÁMETROS DEL MODAL (NUEVO)
    incluir_exp = request.GET.get('exp', 'on') == 'on'
    incluir_cur = request.GET.get('cur', 'on') == 'on'
    incluir_rec = request.GET.get('rec', 'on') == 'on'
    incluir_aca = request.GET.get('aca', 'on') == 'on'
    incluir_lab = request.GET.get('lab', 'on') == 'on'
    incluir_gar = request.GET.get('gar') == 'on'

    # CONSULTAS FILTRADAS (MODIFICADO PARA USAR LOS CHECKS)
    experiencias = ExperienciaLaboral.objects.filter(idperfil=perfil, activarparaqueseveaenfront=True) if incluir_exp else []
    productos_academicos = ProductosAcademicos.objects.filter(idperfil=perfil, activarparaqueseveaenfront=True) if incluir_aca else []
    productos_laborales = ProductosLaborales.objects.filter(idperfil=perfil, activarparaqueseveaenfront=True) if incluir_lab else []
    cursos_objs = CursosRealizados.objects.filter(idperfil=perfil, activarparaqueseveaenfront=True) if incluir_cur else []
    reconocimientos_objs = Reconocimientos.objects.filter(idperfil=perfil, activarparaqueseveaenfront=True) if incluir_rec else []
    
    # NUEVA CONSULTA: GARAGE
    articulos_garage = VentaGarage.objects.filter(idperfil=perfil, activarparaqueseveaenfront=True) if incluir_gar else []
    
    template = get_template('reportes/pdf_personales.html')
    context = {
        'perfil': perfil,
        'items': experiencias,
        'productos': productos_academicos,
        'productos_laborales': productos_laborales,
        'cursos': cursos_objs,
        'reconocimientos': reconocimientos_objs,
        'garage': articulos_garage,  # Enviamos los datos de garage al PDF
    }
    html = template.render(context)
    
    buffer_cv_base = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=buffer_cv_base, link_callback=link_callback)
    
    if pisa_status.err:
        return HttpResponse('Error al generar el cuerpo del PDF', status=500)
    
    writer = PdfWriter()
    buffer_cv_base.seek(0)
    writer.append(buffer_cv_base)

    # UNIÓN DE PDFs CONDICIONAL (Solo si la sección está activa)
    if incluir_cur:
        cursos_con_pdf = [c for c in cursos_objs if c.rutacertificado]
        if cursos_con_pdf:
            writer.append(crear_caratula("Certificados de Cursos"))
            for curso in cursos_con_pdf:
                try:
                    response = requests.get(curso.rutacertificado.url, timeout=15)
                    if response.status_code == 200:
                        writer.append(io.BytesIO(response.content))
                except Exception as e:
                    print(f"Error al descargar curso: {e}")

    if incluir_rec:
        reco_con_pdf = [r for r in reconocimientos_objs if r.rutacertificado]
        if reco_con_pdf:
            writer.append(crear_caratula("Reconocimientos"))
            for reco in reco_con_pdf:
                try:
                    response = requests.get(reco.rutacertificado.url, timeout=15)
                    if response.status_code == 200:
                        writer.append(io.BytesIO(response.content))
                except Exception as e:
                    print(f"Error al descargar reconocimiento: {e}")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="CV_{perfil.apellidos}_Completo.pdf"'
    
    writer.write(response)
    writer.close()
    
    return response